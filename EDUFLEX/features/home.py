import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_local_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def HOME():
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
        lottie_animation2 = load_local_lottie("animations\\animation.json")
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
        lottie_animation2 = load_local_lottie("animations\\animation1.json")
        st_lottie(lottie_animation2, key="courseplan", height=450, width=450)

    col7,col8 = st.columns(2)
    with col7:
        st.markdown("""
                <ul>
                    <li style="font-size:25px ; margin-top:35px"><h3>Curated Video Tutorials :</h3> Enhance your learning experience with our curated selection of video tutorials. Based on your study plan and skill level, we recommend relevant video resources to supplement your learning journey. With EduFlex, you'll have access to high-quality educational content that's both engaging and informative.</li>
                </ul>
                """, unsafe_allow_html=True)
    with col8:
        lottie_animation2 = load_local_lottie("animations\\animation2.json")
        st_lottie(lottie_animation2, key="video", height=400, width=400)

    col9,col10 = st.columns(2)
    with col10:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3>Focused Learning Environment: </h3> We believe in the power of focus. That's why EduFlex integrates a unique feature that blocks irrelevant tabs and distractions while you're engaged in your learning sessions. Say hello to a distraction-free environment where you can concentrate fully on mastering new concepts.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col9:
        lottie_animation2 = load_local_lottie("animations\\animation3.json")
        st_lottie(lottie_animation2, key="focus", height=400, width=400)
    col11, col12 = st.columns(2)
    with col11:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3>Pomodoro Technique Integration:</h3> Boost your productivity and maintain peak performance with the Pomodoro Technique. Our extension includes built-in Pomodoro timers, allowing you to structure your study sessions effectively and optimize learning intervals with short breaks for improved retention.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col12:
        lottie_animation2 = load_local_lottie("animations\\animation4.json")
        st_lottie(lottie_animation2, key="pomodoro", height=400, width=400)

    col13,col14 = st.columns(2)
    with col14:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3> Interactive Chat Support:</h3> Need clarification on a concept? No problem! With our interactive chat support feature, you can engage in real-time conversations with our intelligent chatbot while watching video tutorials. Ask questions, seek guidance, and deepen your understanding—all within the EduFlex platform.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col13:
        lottie_animation2 = load_local_lottie("animations\\animation5.json")
        st_lottie(lottie_animation2, key="chatbot", height=400, width=400)

    col15,col16 = st.columns(2)
    with col15:
       st.markdown("""
                <ul>
                  <li style="font-size:25px ; margin-top:35px"><h3>Skill Testing and Assessment:</h3> Measure your progress and reinforce your learning with our skill testing feature. After completing a video tutorial, take a skill test to evaluate your comprehension and identify areas for improvement. At EduFlex, we're committed to helping you enhance your understanding and achieve academic success.</li>
               </ul>
               """, unsafe_allow_html=True)
    with col16:
        lottie_animation2 = load_local_lottie("animations\\animation6.json")
        st_lottie(lottie_animation2, key="skill-test", height=400, width=400)

    st.markdown("<h1 style='color: #6236ea; text-align:center'>Join EduFlex Today!</h1>", unsafe_allow_html=True)
