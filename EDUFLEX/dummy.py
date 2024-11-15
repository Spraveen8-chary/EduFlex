import json
import urllib.parse
import requests
import streamlit as st
import cv2
import numpy as np
from features.apikeys import *
from pytube import YouTube
from streamlit_clickable_images import clickable_images
from streamlit_option_menu import option_menu
apikey = GEMINIAI_API_KEY
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
from streamlit_lottie import st_lottie
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi
from helpers.quiz import get_quiz_data, get_video_text
from helpers.quiz_utils import string_to_list, get_randomized_options
from helpers.toast_messages import get_random_toast
from urllib.parse import urlparse




st.set_page_config("EDUFLEX",page_icon="🔖",layout="wide")
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_local_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


# Load the certificate template
certificate_template = cv2.imread("certificate_template.jpg")

#logo = Image.open("logo.jpg").convert("RGBA")

logo = cv2.imread("logo.jpg")




# Function to generate the certificate
def generate_certificate(name):
    # Make a copy of the template
    certificate = certificate_template.copy()

    # Add the name to the certificate
    font = cv2.FONT_HERSHEY_TRIPLEX
    text_color = (0, 0, 0)  # Black color
    text_thickness = 5
    text_size, _ = cv2.getTextSize(name, font, 1, text_thickness)
    text_x = 440 - text_size[0] // 2  # Center the text horizontally
    text_y = 490
    cv2.putText(certificate, name, (text_x, text_y), font, 3, text_color, text_thickness)

    # Encode the certificate as PNG
    _, encoded_certificate = cv2.imencode(".png", certificate)
    return encoded_certificate

# Streamlit app
def app():
    #st.image(logo, use_column_width=True)

    with st.sidebar:

        #st.image(logo, use_column_width=True)
        lottie_animation2 = load_local_lottie("logo_animation.json")
        st_lottie(lottie_animation2, key="logo", height=150, width=150)
        #st.markdown('<style>img { width: 150px; height: 150px; } </style>', unsafe_allow_html=True)
        #st.image(logo)
        markdown_text = """
        - Had you course completed ? Get your certificate from :blue[Eduflex] Today👇👇.
        """
        st.markdown(markdown_text)
        #st.title("Certificate Generator")

        # Get the student's name
        name = st.text_input("Enter the student's name")

        if name:
            # Generate the certificate
            certificate_bytes = generate_certificate(name)

            # Display the certificate
            st.image(certificate_bytes.tobytes(), channels="BGR")

            # Download button
            st.download_button(
                label="Download Certificate",
                data=certificate_bytes.tobytes(),
                file_name=f"{name}_certificate.png",
                mime="image/png",
            )
if __name__ == "__main__":
    app()

os.environ["GOOGLE_API_KEY"] = GEMINIAI_API_KEY

genai.configure(api_key=apikey)

chosen = option_menu(
    menu_title=None,
    options = ["Welcome","Learn","Skill Test","Road Map","Get Materials"],
    icons = ["snow3","bi-book-half","clipboard2-data","clipboard2-check","book"],
    default_index=0,
    orientation="horizontal")

if chosen == "Welcome":
    st.title("Welcome to :blue[EduFlex]: Your Personalized Learning Companion 📚 ")




    lottie_animation1 = "https://lottie.host/cca84fef-b871-48c8-a756-ab0f3f17fcd5/hjJGMFluMT.json"
    lottie_anime_json = load_lottie(lottie_animation1)

    col1,col2 = st.columns(2)
    with col1:
        st_lottie(lottie_anime_json,key="student",height=400,width=400)
    with col2:

        # Display bullet points using HTML syntax
        st.markdown("""
        <ul>
          <li style="font-size:25px ; margin-top:35px">At EduFlex, we revolutionize the way you learn by tailoring every aspect of your educational journey to your unique needs and preferences. Our comprehensive platform offers a seamless blend of innovative features designed to maximize your learning potential and achieve your academic goals effortlessly.</li>
        </ul>
        """, unsafe_allow_html=True)
    col3,col4 = st.columns(2)
    with col4:
        lottie_animation2 = load_local_lottie("animation.json")
        st_lottie(lottie_animation2,key="study",height=400,width=400)
    with col3:

        # Display bullet points using HTML syntax
        st.markdown("""
        <ul>
          <li style="font-size:23px ; margin-top:80px">Personalized Study Plans</li>
          <li style="font-size:23px">Curated Video Tutorials</li>
          <li style="font-size:23px">Focused Learning Environment</li>
          <li style="font-size:23px">Pomodoro Technique Integration</li>
          <li style="font-size:23px">Interactive Chat Support</li>
          <li style="font-size:23px">Skill Testing and Assessment</li>
        </ul>
        """, unsafe_allow_html=True)

    col5 , col6 = st.columns(2)

    with col6:
        st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3>Personalized Study Plans</h3> Say goodbye to one-size-fits-all approaches! With EduFlex, we understand that every learner is different. That's why we gather essential information from you and craft a customized study plan meticulously tailored to your schedule and learning objectives. Whether you're a beginner, intermediate, or advanced learner, we've got you covered.</li>
                </ul>
                """, unsafe_allow_html=True)
    with col5:
        lottie_animation2 = load_local_lottie("animation1.json")
        st_lottie(lottie_animation2, key="courseplan", height=450, width=450)

    col7,col8 = st.columns(2)
    with col7:
        st.markdown("""
                <ul>
                    <li style="font-size:25px ; margin-top:35px"><h3>Curated Video Tutorials :</h3> Enhance your learning experience with our curated selection of video tutorials. Based on your study plan and skill level, we recommend relevant video resources to supplement your learning journey. With EduFlex, you'll have access to high-quality educational content that's both engaging and informative.</li>
                </ul>
                """, unsafe_allow_html=True)
    with col8:
        lottie_animation2 = load_local_lottie("animation2.json")
        st_lottie(lottie_animation2, key="video", height=400, width=400)

    col9,col10 = st.columns(2)
    with col10:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3>Focused Learning Environment: </h3> We believe in the power of focus. That's why EduFlex integrates a unique feature that blocks irrelevant tabs and distractions while you're engaged in your learning sessions. Say hello to a distraction-free environment where you can concentrate fully on mastering new concepts.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col9:
        lottie_animation2 = load_local_lottie("animation3.json")
        st_lottie(lottie_animation2, key="focus", height=400, width=400)
    col11, col12 = st.columns(2)
    with col11:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3>Pomodoro Technique Integration:</h3> Boost your productivity and maintain peak performance with the Pomodoro Technique. Our extension includes built-in Pomodoro timers, allowing you to structure your study sessions effectively and optimize learning intervals with short breaks for improved retention.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col12:
        lottie_animation2 = load_local_lottie("animation4.json")
        st_lottie(lottie_animation2, key="pomodoro", height=400, width=400)

    col13,col14 = st.columns(2)
    with col14:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3> Interactive Chat Support:</h3> Need clarification on a concept? No problem! With our interactive chat support feature, you can engage in real-time conversations with our intelligent chatbot while watching video tutorials. Ask questions, seek guidance, and deepen your understanding—all within the EduFlex platform.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col13:
        lottie_animation2 = load_local_lottie("animation5.json")
        st_lottie(lottie_animation2, key="chatbot", height=400, width=400)

    col15,col16 = st.columns(2)
    with col15:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3>Skill Testing and Assessment:</h3> Measure your progress and reinforce your learning with our skill testing feature. After completing a video tutorial, take a skill test to evaluate your comprehension and identify areas for improvement. At EduFlex, we're committed to helping you enhance your understanding and achieve academic success.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col16:
        lottie_animation2 = load_local_lottie("animation6.json")
        st_lottie(lottie_animation2, key="skill-test", height=400, width=400)



    st.markdown("<h1 style='color: #6236ea; text-align:center'>Join EduFlex Today!</h1>", unsafe_allow_html=True)

if chosen == "Learn":

    st.title("Course recommender")
    # Replace 'YOUTUBE_API_KEY' with your actual API key
    API_KEY = "AIzaSyCtzlv23kCbEdM9tQM4hE1EXa2gSXbrkWQ"
    # API_KEY = YOUTUBE_API_KEY


    @st.cache_data
    # Function to search for videos based on a query
    def search_videos(query, max_results=6):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={urllib.parse.quote(query)}&type=video&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        video_links = [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in data['items']]
        return video_links

    # Ask user for search query
    c1,c2 = st.columns(2)
    with c1:
        query = st.text_input("What do you want to learn")
    with c2:
        level = st.selectbox("Choose your learning level", ["Beginner", "Intermediate", "Advanced"])

    full_query = f"{query} {level} full course"
    videos = search_videos(full_query)
    links = []
    #print("YouTube Links:")
    for video in videos:
        links.append(video)

    @st.cache_data
    def youtube(url):
        yt = YouTube(url)
        return yt.title,yt.thumbnail_url

    titles = []
    locations=[]
    thumbnails = []

    for video_url in links:
        video_title , video_thumbnail = youtube(video_url)
        titles.append(video_title)
        thumbnails.append(video_thumbnail)
    if query:
            selected_video = clickable_images(thumbnails,
                        titles=titles,div_style={"height": "500px","display": "grid", "grid-template-columns":"repeat(2,1fr)" ,"justify-content": "center","align-item":"center",
                        "flex-wrap": "nowrap", "overflow-y": "auto"},
                        img_style={"margin": "10px", "height": "250px"})
            st.markdown(f"Thumbnail #{selected_video} clicked" if selected_video >-1 else None)
            col1,col2 = st.columns(2)
            with col1:
                if selected_video > -1:
                    video_url = links[selected_video]
                    video_title = titles[selected_video]

                    st.header(video_title)
                    st.video(video_url)
            with col2:
                if "notes" not in st.session_state:
                    st.session_state["notes"] = []


                def add_note(note_text):
                    if note_text:
                        st.session_state["notes"].append(note_text)
                        st.success("Note added successfully!")
                    else:
                        st.warning("Please enter a note before adding.")


                def display_notes():
                    if st.session_state["notes"]:
                        st.header("Your Notes:")
                        for note in st.session_state["notes"]:
                            st.write(note)
                        st.button("Clear Notes", on_click=st.session_state["notes"].clear)  # Clear notes on click
                    else:
                        st.info("No notes added yet.")

                st.markdown("")
                st.markdown("")
                st.markdown("")
                #st.markdown("")
                #st.markdown("")
                #st.markdown("")
                st.header("Take Notes")
                note_text = st.text_area("Write a note:", height=200)
                add_note_button = st.button("Add Note")

                if add_note_button:
                    add_note(note_text)
                    st.empty()  # Clear note input for better UX

                display_notes_button = st.button("Display All Notes")
                if display_notes_button:
                    display_notes()
            col1,col2=st.columns(2)
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

                            transcript = ""
                            for i in transcript_text:
                                transcript += " " + i['text']

                            return transcript

                        except Exception as e:
                            raise e


                    def get_pdf_text(pdf_docs):
                        text = ""
                        for pdf in pdf_docs:
                            pdf_reader = PdfReader(pdf)
                            for page in pdf_reader.pages:
                                text += page.extract_text()
                        return text


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
                        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

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

                        print(response)
                        st.write(response["output_text"])


                    def main():
                        #st.set_page_config("Chat PDF")
                        st.header("Chat with Youtube Video💁")

                        user_question = st.text_input(f"Ask a Question from the {video_title} ")

                        if user_question:
                            user_input(user_question)



                        #video_url = st.text_input("Upload the youtube video link here")
                        #if st.button("Submit & Process"):
                        with st.spinner("Processing..."):
                            raw_text = get_video_text(video_url)
                            text_chunks = get_text_chunks(raw_text)
                            get_vector_store(text_chunks)
                            st.success("Done")


                    if __name__ == "__main__":
                        main()
                except Exception as e:
                    print(e)


if chosen == "Skill Test":

    os.environ["GOOGLE_API_KEY"] = "AIzaSyCswPVrlnUZoWLig2VlF3Hj0p7pJBuOoTE"
    genai.configure(api_key="AIzaSyCswPVrlnUZoWLig2VlF3Hj0p7pJBuOoTE")
    st.title("Start taking Skill Test from the skills you have learnt")

    # Check if user is new or returning using session state.
    # If user is new, show the toast message.
    if 'first_time' not in st.session_state:
        message, icon = get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False

    st.title(":red[QuizBuddy] — Learn.Quiz.Practice  🧠", anchor=False)

    with st.form("user_input"):
        cl1, cl2 = st.columns(2)
        with cl1:
            skill = st.text_input("Enter the skill that you want to take the test")
        cl3, cl4 = st.columns(2)
        with cl3:
            skill_level = st.selectbox("At which level are you in the skill", ["Beginner", "Intermediate", "Advanced"])
        with cl2:
            skill_topic = st.text_input("On what topic in skill you want to take on?")
        with cl4:
            number_of_questions = st.number_input("Choose number of questions", value=1)
        number_of_questions = str(number_of_questions)
        # YOUTUBE_URL = st.text_input("Enter the YouTube video link:")
        # OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password')
        submitted = st.form_submit_button("Craft my quiz!")

    if submitted or ('quiz_data_list' in st.session_state):

        with st.spinner("Crafting your quiz...🤓"):
            if submitted:
                # video_id = extract_video_id_from_url(YOUTUBE_URL)
                quiz_data_str = get_quiz_data(skill_topic, skill_level, skill_topic, number_of_questions)
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

                                apikey = GEMINI_API_KEY

                                os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY
                                

                                # text = get_video_text(YOUTUBE_URL)
                                quiz_data = " ".join(map(str, st.session_state.quiz_data_list))

                                prompt_template = f"""This is the question that is generated with the inputs of {skill} the user want to take test 
                                                    in the particular {skill_topic} with the his level of understanding at {skill_level} level.These are the 
                                                    questions that are generated {quiz_data} with the inputs the user have given.User have chosen the option {ro[ua]}.
                                                    But the correct option is {ca}.I want you to write a short and crisp explation why is {ca} is the correct option since you are an expert in {skill}."""
                                model = genai.GenerativeModel("gemini-pro")
                                response = model.generate_content(
                                    prompt_template + skill + skill_level + skill_topic + q[0] + quiz_data + ro[
                                        ua] + ca)
                                st.info(response.text)

if chosen == "Road Map":

   
    apikey = GEMINIAI_API_KEY
    os.environ['GOOGLE_API_KEY'] = GEMINIAI_API_KEY
    genai.configure(api_key=apikey)

    st.title("Daily Course Planner")

    # Using a form to submit user inputs
    #form = st.form("course_planner_form")
    with st.form("user_input"):
        name = st.text_input("Please tell us your name")

        col1, col2 = st.columns(2)
        with col1:
            course = st.text_input("Which course do you want to learn")
        with col2:
            learning_level = st.selectbox("Choose your level of learning",
                                              ["Beginner", "Intermediate", "Advanced"])

        col3, col4 = st.columns(2)
        with col3:
            no_of_hours = st.number_input("Choose number of learning hours per day",
                                              value=1, placeholder="Choose here")
        with col4:
            no_of_days = st.number_input("How many days you want to learn the skill",
                                             value=1, placeholder="Choose here")

        target_level = st.selectbox(
            "To which level do you want to reach at the end of the preparation",
            ["Intermediate", "Advanced"])

        # Submit button to submit the form
        submit = st.form_submit_button("Submit")


    if submit:
        with st.spinner(text="Processing..."):
            prompt_template = f'''You are course a lecture in the course.{course}I am you student who want to learn the course that you teach.
                                    I am at this {learning_level}.I want to learn the course in {no_of_days} days by spending {no_of_hours} hours daily.
                                    At the end of the preparation I need to reach {target_level}.As a lecturer in  the {course} I want a daily plan
                                    to follow to learn that course.Give me the plan according to the inputs that I have provided to reach the {target_level}.
                                    Tell me where I have to start at the start of the day and the topics that I have to cover in the day and at what timings.
                                    At the end of the day I want to revise the topics that  I have learnt at the end of the day so please add the revision time and the
                                    topics to recall. Start the plan with a motivational quote so that I can have a positive attitude while learning.Add the timings in which
                                    to complete the topic.I cannot spend all {no_of_hours} hours at once so divide them in the day at each part of the day.
                                    Output Format :
                                    DAY_1 :
                                    9-10 : Topics to Cover
                                    10-11 : Topics to cover.
                                    ""
                                    ""
                                    Always the output should be properly formatted with proper headings and highlightings.
             
                                    '''
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt_template)
            plan = response.text
            st.markdown(plan)

            # Save button to save the plan to a text file
            st.download_button(
                label="Download plan as text",
                data=plan,
                file_name=f"{course}_{no_of_days}_day_plan.txt",
                mime="text/plain",
            )

    

if chosen=="Get Materials":

    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

    api_key = GOOGLE_API_KEY

    search_engine_id = SEARCH_ID

    markdown_text = """
    # Course Materials

    Welcome to our Course Materials section! Here, you can find a wealth of resources tailored to your learning needs. Whether you're a beginner, intermediate, or advanced learner, we've got you covered. Simply enter your query below, and we'll provide you with relevant materials to help you excel in your studies.

    ## How to Use

    1. **Enter Your Query**: Type your topic or keyword of interest in the search box below.
    2. **Explore Resources**: Once you've entered your query, hit the "Search" button, and we'll fetch the most relevant materials for you.
    3. **Learn and Grow**: Dive into the materials provided, including articles, videos, tutorials, and more, to enhance your understanding and mastery of the subject.

    """

    # Display Markdown text in the app
    st.markdown(markdown_text)

    col1,col2,col3 = st.columns(3)
    with col2:
        search_query = st.text_input("On which topic do you need materials")

    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_query,
        'key': api_key,
        'cx': search_engine_id,
        'fileType': 'pdf'
    }

    if search_query:
        response = requests.get(url, params=params)
        results = response.json()['items']
        pdf_links = []
        for item in results:
            # print(item['link'])
            pdf_links.append(item['link'])



        def get_domain_name(url):
            """
            Extracts the domain name from a given URL and removes the "www" prefix if present.
            """
            parsed_url = urlparse(url)
            domain_name = parsed_url.netloc
            if domain_name.startswith("www."):
                domain_name = domain_name[4:]
            return domain_name


        def display_pdf_links(pdf_links):

            for link in pdf_links:
                domain_name = get_domain_name(link)
                # st.subheader(domain_name)
                st.subheader(f"[{domain_name}]({link})")
                # st.write(f"[Link]({link})")

        st.write(":green[Here are the materials that we have found online related to your query]👇👇")
        display_pdf_links(pdf_links)


