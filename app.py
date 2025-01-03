import streamlit as st
import json
import cv2
import time
import hashlib
import uuid

from streamlit_option_menu import option_menu
import google.generativeai as genai
from streamlit_lottie import st_lottie
from features.apikeys import GEMINIAI_API_KEY
from features.home import HOME, load_local_lottie
from features.certificate_generation import generate_certificate
from features.course import LEARN
from features.test import TEST
from features.roadmap import ROADMAP
from features.materials import GET_MATERIAL
from features.compiler import code_with_ai
from connect_database import login, register_account
from features.pdfchat import PDF_CHAT

def generate_numeric_id(data, range_limit=100):
    data_with_timestamp = f"{data}{time.time()}"
    hash_object = hashlib.md5(data_with_timestamp.encode())
    hex_digest = hash_object.hexdigest()
    numeric_id = int(hex_digest, 16)
    result_id = numeric_id % range_limit
    return result_id

unique_id = uuid.uuid4()
numeric_id = int(str(unique_id)[:8], 16)

st.set_page_config("EDUFLEX", page_icon="🔖", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "login"  

logo = cv2.imread("animations\\logo.jpg")

def app():
    with st.sidebar:
        lottie_animation2 = load_local_lottie("animations\\logo_animation.json")
        st_lottie(lottie_animation2, key="logo", height=150, width=150)

        markdown_text = """
        - Had you course completed? Get your certificate from :blue[Eduflex] Today👇👇.
        """
        st.markdown(markdown_text)

        name = st.text_input("Enter the student's name")

        if name:
            certificate_bytes = generate_certificate(name)
            st.image(certificate_bytes.tobytes(), channels="BGR")
            st.download_button(
                label="Download Certificate",
                data=certificate_bytes.tobytes(),
                file_name=f"{name}_certificate.png",
                mime="image/png",
            )

genai.configure(api_key=GEMINIAI_API_KEY)

def load_lottie_animation(path):
    with open(path, "r") as f:
        return json.load(f)

def login_page():
    st.title("Login to Eduflex")

    lottie_animation = load_lottie_animation(r"D:\EDUFLEX\animations\login animation.json")
    col1, col2 = st.columns([1, 1])

    with col1:
        st_lottie(lottie_animation, height=300, key="login_animation")

    with col2:
        st.subheader("Login")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        if st.button("Login", key="login_button"):
            if email and password and login(email=email, password=password):
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.session_state["active_page"] = "home"  
                    st.rerun()
            else:
                st.error("Please enter both email and password.")

def register_page():
    st.title("Register for Eduflex")

    lottie_animation = load_lottie_animation(r"D:\EDUFLEX\animations\login animation.json")
    col1, col2 = st.columns([1, 1])

    with col1:
        st_lottie(lottie_animation, height=300, key="register_animation")

    with col2:
        st.subheader("Create a New Account")
        first_name = st.text_input("First Name", placeholder="Enter your first name")
        last_name = st.text_input("Last Name", placeholder="Enter your last name")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Create a password", type="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Re-enter your password", type="password")

        if st.button("Register", key="register_button"):
            if first_name and last_name and email and password and confirm_password:
                if password == confirm_password:
                    if register_account(fname=first_name, lname= last_name, email=email, password=password, ids=generate_numeric_id(numeric_id, range_limit=26)):  
                        st.success("Registration successful! Please log in.")
                        st.session_state["active_page"] = "login"  
                    else:
                        st.error("Registration failed. Try again.")
                else:
                    st.error("Passwords do not match.")
            else:
                st.error("Please fill in all fields.")

def top_navigation():
    col1, col2, col3 = st.columns([4, 2, 4])  

    with col2:  
        if not st.session_state["logged_in"]:
            col_btn1, col_btn2 = st.columns(2) 
            with col_btn1:
                if st.button("Login", key="sidebar_login_button"):
                    st.session_state["active_page"] = "login"
            with col_btn2:
                if st.button("Register", key="sidebar_register_button"):
                    st.session_state["active_page"] = "register"


def main_app():
    chosen = option_menu(
        menu_title=None,
        options=["Welcome", "Learn", "Skill Test", "Road Map", "Get Materials", "Compiler", "PDF Chat"],
        icons=["snow3", "bi-book-half", "clipboard2-data", "clipboard2-check", "book", "code", "book"],
        default_index=0,
        orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "blue"}})

    if chosen == "Welcome":
        app()
        HOME()
    elif chosen == "Learn":
        LEARN()
    elif chosen == "Skill Test":
        TEST()
    elif chosen == "Road Map":
        ROADMAP()
    elif chosen == "Get Materials":
        GET_MATERIAL()
    elif chosen == "Compiler":
        code_with_ai()
    elif chosen == "PDF Chat":
        PDF_CHAT()
    

def page_routing():
    if st.session_state["active_page"] == "login":
        login_page()
    elif st.session_state["active_page"] == "register":
        register_page()
    elif st.session_state["logged_in"]:
        main_app()

top_navigation()
page_routing()
