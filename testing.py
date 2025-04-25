import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from google.generativeai import GenerativeModel
import pyttsx3
import tempfile
import os
import av
import queue
import torch
import torchaudio
import numpy as np
import wave
import google.generativeai as genai
import threading
import time
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

tts_engine = pyttsx3.init()
tts_lock = threading.Lock()  
audio_queue = queue.Queue()

QUESTIONS = {
    "Software Development": {
        "Beginner": [
            "What is a variable?",
            "Explain the concept of a function.",
            "What is a loop?"
        ],
        "Intermediate": [
            "What is polymorphism?",
            "Explain the difference between a list and a tuple.",
            "What are decorators in Python?"
        ],
        "Advanced": [
            "Explain the concept of concurrency.",
            "What is dependency injection?",
            "How do you optimize database queries?"
        ]
    }
}

def audio_frame_callback(frame: av.AudioFrame):
    audio = frame.to_ndarray()
    audio_queue.put(audio)
    return frame

def speak_text(text):
    def run():
        with tts_lock:
            tts_engine.say(text)
            tts_engine.runAndWait()

    threading.Thread(target=run).start()

def save_audio(frames, filename):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

def transcribe_audio(audio_path):
    # Dummy Gemini call placeholder
    # Replace with proper Gemini speech-to-text when available
    return "This is a dummy transcription."

def chat_with_ai(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    st.title("🧠 AI-Based Interview System (Gemini-Powered)")

    st.sidebar.header("Interview Configuration")
    domain = st.sidebar.selectbox("Select Domain", list(QUESTIONS.keys()))
    level = st.sidebar.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
    start_button = st.sidebar.button("Start Interview")

    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = []

    if start_button:
        st.session_state.interview_started = True
        st.session_state.current_q = 0
        st.session_state.scores = []

    if st.session_state.interview_started:
        webrtc_streamer(
            key="interview",
            mode=WebRtcMode.SENDRECV,
            audio_frame_callback=audio_frame_callback,
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True
        )

        questions = QUESTIONS[domain][level]

        if st.session_state.current_q < len(questions):
            q = questions[st.session_state.current_q]
            st.subheader(f"Question {st.session_state.current_q + 1}")
            st.write(q)
            speak_text(q)

            if st.button("Submit Answer"):
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                collected = []
                while not audio_queue.empty():
                    collected.append(audio_queue.get().tobytes())
                save_audio(collected, temp_audio.name)

                answer_text = transcribe_audio(temp_audio.name)
                st.write("Transcribed Answer:", answer_text)

                ai_response = chat_with_ai(f"Q: {q} A: {answer_text}. Evaluate this answer in terms of clarity, correctness, and depth.")
                st.session_state.scores.append(ai_response)

                os.unlink(temp_audio.name)

                st.session_state.current_q += 1
                st.experimental_rerun()
        else:
            st.success("Interview Completed!")
            for idx, score in enumerate(st.session_state.scores, 1):
                st.markdown(f"**Q{idx} Evaluation:** {score}")

            if st.button("Restart Interview"):
                st.session_state.interview_started = False
                st.session_state.current_q = 0
                st.session_state.scores = []
                st.experimental_rerun()

if __name__ == "__main__":
    main()
