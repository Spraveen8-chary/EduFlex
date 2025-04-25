import os
import streamlit as st
from features.logger import log_action
from streamlit_clickable_images import clickable_images
from features.apikeys import GEMINIAI_API_KEY, YOUTUBE_API_KEY
import requests
import urllib.parse
import google.generativeai as genai
from pytube import YouTube
from pytube.exceptions import PytubeError 
from youtube_transcript_api import YouTubeTranscriptApi
from streamlit_option_menu import option_menu
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


def LEARN(username = ""):
    st.title("Course Recommender")
    API_KEY = YOUTUBE_API_KEY

    @st.cache_data
    # Function to search for videos based on a query
    def search_videos(query, max_results=6):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={urllib.parse.quote(query)}&type=video&key={API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Debug: Check if there are items in the response
        if 'items' not in data:
            st.error("No videos found. Please try a different search query.")
            return []

        video_data = []
        log_action(username, f"Recommended Videos for '{query}': ")
        for item in data['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_data.append({
                "title": title,
                "thumbnail": thumbnail_url,
                "url": video_url
            })
            log_action(username, f"{title}")

        return video_data

    # Ask user for search query
    c1, c2 = st.columns(2)
    with c1:
        query = st.text_input("What do you want to learn?")
    with c2:
        level = st.selectbox("Choose your learning level", ["Beginner", "Intermediate", "Advanced"])

    full_query = f"{query} {level} full course"
    videos = search_videos(full_query)

    if not videos:
        return  # Stop if no videos were found

    titles = [video["title"] for video in videos]
    thumbnails = [video["thumbnail"] for video in videos]
    links = [video["url"] for video in videos]

    # Display clickable images with thumbnails
    if query:
        selected_video = clickable_images(
            thumbnails,
            titles=titles,
            div_style={
                "height": "450px",
                "widht" : "600px",
                "display": "grid",
                "grid-template-columns": "repeat(2, 1fr)",
                "justify-content": "center",
                "align-items": "center",
                "flex-wrap": "nowrap",
                "overflow-y": "auto"
            },
            img_style={"margin": "10px", "height": "450px"}
        )
        print("Selected Video : ", selected_video)
        col1, col2 = st.columns(2)
        # Show selected video details and embed video
        with col1:
            if selected_video is not None and selected_video > -1:
                video_url = links[selected_video]
                print(video_url)
                video_title = titles[selected_video]

                log_action(username, f"Selected Video : '{selected_video}', '{video_title}'")

                st.markdown(f"### {video_title}")
                st.video(video_url)

            with col2:
                if "notes" not in st.session_state:
                    st.session_state["notes"] = []


                def add_note(note_text):
                    if note_text:
                        st.session_state["notes"].append(note_text)
                        st.success("Note added successfully!")
                        log_action(username, "Note added")
                    else:
                        st.warning("Please enter a note before adding.")
                        log_action(username, "Error while adding Note", "warning")


                def display_notes():
                    if st.session_state["notes"]:
                        st.header("Your Notes:")
                        for note in st.session_state["notes"]:
                            st.write(note)
                            log_action(username, "Note Displayed")
                        st.button("Clear Notes", on_click=st.session_state["notes"].clear)  # Clear notes on click
                    else:
                        st.info("No notes added yet.")
                        log_action(username, "Note not Displayed")

                st.markdown("")
                st.markdown("")
                st.markdown("")

                st.header("Take Notes")
                note_text = st.text_area("Write a note:", height=200)
                add_note_button = st.button("Add Note")

                if add_note_button:
                    add_note(note_text)
                    st.empty()  

                display_notes_button = st.button("Display All Notes")
                if display_notes_button:
                    display_notes()
            col1,col2=st.columns(2)
            # st.markdown("")
            # st.markdown("")
            # st.markdown("")
            # st.markdown("### Chat with Video")
            with col2:
                st.markdown("")
                st.markdown("")
                st.markdown("")
                chat_with_video = option_menu(
                                menu_title=None,
                                options = ["Chat with Video"],
                                icons = ['alexa'],
                                default_index=0,
                                )
            if chat_with_video=="Chat with Video":

                try:
                    apikey = GEMINIAI_API_KEY
                    os.environ["GOOGLE_API_KEY"] = GEMINIAI_API_KEY
                    genai.configure(api_key=apikey)


                    @st.cache_data
                    def get_video_text(video_url):
                        try:
                            video_id = video_url.split("=")[1]
                            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

                            transcript = " ".join([item["text"] for item in transcript_text])
                            return transcript

                        except Exception as e:
                            raise e

                    @st.cache_data
                    def get_text_chunks(text):
                        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
                        chunks = text_splitter.split_text(text)
                        return chunks


                    @st.cache_data
                    def get_vector_store(text_chunks):
                        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
                        vector_store.save_local("faiss_index")


                    
                    def get_conversational_chain():
                        prompt_template = '''Answer the question as detailed as possible from the provided context, make sure to provide all the details.
                        Context:\n {context}?\n
                        Question: \n{question}\n
        
                        Answer:
                        '''
                        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

                        prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'questions'])
                        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

                        return chain


                    def user_input(user_question):
                        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

                        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
                        docs = new_db.similarity_search(user_question)
 
                        chain = get_conversational_chain()

                        response = chain({
                            "input_documents": docs, "question": user_question
                        },
                            return_only_outputs=True)

                        st.write(response["output_text"])
                        log_action(username, f"AI Explained about => '{user_question}'")
                        


                    st.markdown("## Chat with the Video!")
                    st.markdown("This allows you to interact with the video content.")
                    
                    # Input field for user question
                    user_question = st.text_input(f"Ask a Question about the {video_title}")

                    # Process the video transcript and create embeddings
                    with st.spinner("Processing video transcript..."):
                        transcript_text = get_video_text(video_url)
                        text_chunks = get_text_chunks(transcript_text)
                        get_vector_store(text_chunks)
                        st.success("Transcript processed! You can now ask questions.")
                        log_action(username, "Transcript processed for selected video! You can now ask questions.")

                    # Handle user question
                    if user_question:
                        user_input(user_question)

                except Exception as e:
                    st.markdown("Their is problem in the video Transcription")
                    log_action(username, "Their is problem in the video Transcription","warning")
                    

if __name__=='__main__':
    LEARN()