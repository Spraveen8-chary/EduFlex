import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import YoutubeLoader
from apikey import geminiai_api_key
apikey = geminiai_api_key
from youtube_transcript_api import YouTubeTranscriptApi

os.environ["GOOGLE_API_KEY"] = geminiai_api_key

genai.configure(api_key=apikey)

import streamlit as st
import requests
import urllib.parse
from pytube import YouTube

API_KEY = "AIzaSyBCE84dh4QtBa3y6hRFktbfM4j7J9hFdlU"



@st.cache_data
# Function to search for videos based on a query
def search_videos(query, max_results=6):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={urllib.parse.quote(query)}&type=video&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    video_links = [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in data['items']]
    return video_links

# Function to retrieve YouTube video title and thumbnail
@st.cache_data
def youtube(url):
    yt = YouTube(url)
    return yt.title, yt.thumbnail_url

# Ask user for search query
query = st.text_input("What do you want to learn")
level = st.selectbox("Choose your learning level", ["Beginner", "Intermediate", "Advanced"])

if query and level:
    full_query = f"{query} {level} full course"
    videos = search_videos(full_query)
    links = []

    for video in videos:
        links.append(video)

    titles = []
    thumbnails = []
    url_link = []

    for video_url in links:
        video_title, video_thumbnail = youtube(video_url)
        titles.append(video_title)
        thumbnails.append(video_thumbnail)
        url_link.append(video_url)


    selected_title = st.selectbox("Select a video", titles)

    index = titles.index(selected_title)

    video_link = url_link[index]

    import streamlit as st
    from helpers.new1 import get_quiz_data, get_video_text

    from helpers.quiz_utils import string_to_list, get_randomized_options
    from helpers.toast_messages import get_random_toast



    # Check if user is new or returning using session state.
    # If user is new, show the toast message.
    if 'first_time' not in st.session_state:
        message, icon = get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False

    st.title(":red[QuizTube] — Watch. Learn. Quiz. 🧠", anchor=False)

    with st.form("user_input"):
        #YOUTUBE_URL = st.text_input("Enter the YouTube video link:")
        # OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password')
        submitted = st.form_submit_button("Craft my quiz!")

    if submitted or ('quiz_data_list' in st.session_state):

        with st.spinner("Crafting your quiz...🤓"):
            if submitted:
                # video_id = extract_video_id_from_url(YOUTUBE_URL)
                video_transcription = get_video_text(video_link)
                quiz_data_str = get_quiz_data(video_transcription)
                st.session_state.quiz_data_list = string_to_list(quiz_data_str)

                if 'user_answers' not in st.session_state:
                    st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
                if 'correct_answers' not in st.session_state:
                    st.session_state.correct_answers = []
                if 'randomized_options' not in st.session_state:
                    st.session_state.randomized_options = []

                for q in st.session_state.quiz_data_list:
                    options, correct_answer = get_randomized_options(q[1:])
                    st.session_state.randomized_options.append(options)
                    st.session_state.correct_answers.append(correct_answer)

            with st.form(key='quiz_form'):
                st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
                for i, q in enumerate(st.session_state.quiz_data_list):
                    options = st.session_state.randomized_options[i]
                    default_index = st.session_state.user_answers[i] if st.session_state.user_answers[
                                                                            i] is not None else 0
                    response = st.radio(q[0], options, index=default_index)
                    user_choice_index = options.index(response)
                    st.session_state.user_answers[
                        i] = user_choice_index  # Update the stored answer right after fetching it

                results_submitted = st.form_submit_button(label='Unveil My Score!')

                if results_submitted:
                    score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in
                                 enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                    st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                    if score == len(st.session_state.quiz_data_list):  # Check if all answers are correct
                        st.balloons()
                    else:
                        incorrect_count = len(st.session_state.quiz_data_list) - score
                        if incorrect_count == 1:
                            st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                        else:
                            st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                    for i, (ua, ca, q, ro) in enumerate(
                            zip(st.session_state.user_answers, st.session_state.correct_answers,
                                st.session_state.quiz_data_list, st.session_state.randomized_options)):
                        with st.expander(f"Question {i + 1}", expanded=False):
                            if ro[ua] != ca:
                                st.info(f"Question: {q[0]}")
                                st.error(f"Your answer: {ro[ua]}")
                                st.success(f"Correct answer: {ca}")

                                import google.generativeai as genai
                                from apikey import gemini_api_key
                                import os

                                apikey = gemini_api_key

                                os.environ['GOOGLE_API_KEY'] = gemini_api_key
                                from helpers.new1 import get_video_text

                                text = get_video_text(YOUTUBE_URL)
                                quiz_data = " ".join(map(str, st.session_state.quiz_data_list))

                                prompt = f"""This is the questions {q[0]} generated with this context {text} and these are the options 
                                            that are generated {quiz_data}.User have choosen the option {ro[ua]}.
                                            But the correct option is {ca}.I want you to write why is the {ca} is the right option by completely analyzing the context you were provided."""

                                model = genai.GenerativeModel("gemini-pro")
                                response = model.generate_content(prompt + q[0] + text + quiz_data + ro[ua] + ca)
                                st.info(response.text)






