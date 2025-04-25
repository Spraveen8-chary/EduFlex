import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.web.cli as stcli
import sys
import json
import cv2
import time
import hashlib
import uuid
from features.logger import log_action

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
from database.connect_database import login, register_account
from features.pdfchat import PDF_CHAT
from features.dashboard import * 

st.set_page_config("EDUFLEX", page_icon="🔖", layout="wide")


def generate_numeric_id(data, range_limit=100):
    data_with_timestamp = f"{data}{time.time()}"
    hash_object = hashlib.md5(data_with_timestamp.encode())
    hex_digest = hash_object.hexdigest()
    numeric_id = int(hex_digest, 16)
    result_id = numeric_id % range_limit
    return result_id

unique_id = uuid.uuid4()
numeric_id = int(str(unique_id)[:8], 16)


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "login"  


logo = cv2.imread("animations\\logo.jpg")

def app():
    user_email = st.session_state.get("user_email", None)

    with st.sidebar:

        if st.button(label="Dashboard"):
            st.session_state["current_page"] = "dashboard"
            st.session_state["user_email"] = user_email
            # st.switch_page(DASHBOARD(user=user_email))  
        if st.session_state.get("current_page") == "dashboard":
            DASHBOARD(user=st.session_state.get("user_email"))
        try:
            lottie_animation2 = load_local_lottie("animations\\logo_animation.json")
            st_lottie(lottie_animation2, key="logo", height=150, width=150)
        except Exception as e:
            log_action(st.session_state["user_email"],f"Failed to load sidebar animation: {e}","warning")

        markdown_text = """
        - Had you course completed? Get your certificate from :blue[Eduflex] Today👇👇.
        """
        st.markdown(markdown_text)

        name = st.text_input("Enter the student's name")

        if name:
            try:
                certificate_bytes = generate_certificate(name)
                st.image(certificate_bytes.tobytes(), channels="BGR")
                st.download_button(
                    label="Download Certificate",
                    data=certificate_bytes.tobytes(),
                    file_name=f"{name}_certificate.png",
                    mime="image/png",
                )
                log_action(st.session_state["user_email"], f"Certificate generated for '{name}'","info")
            except Exception as e:
                log_action(st.session_state["user_email"],f"Error generating certificate for '{name}': '{e}'", "warning")

genai.configure(api_key=GEMINIAI_API_KEY)

def load_lottie_animation(path):
    with open(path, "r") as f:
        return json.load(f)

def login_page():
    st.title("Login to Eduflex")
    log_action(st.session_state["user_email"],"Login page accessed", "info")

    lottie_animation = load_lottie_animation("animations//login animation.json")
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
                    log_action(st.session_state["user_email"],f"User '{email}' logged in successfully", "info")
                    st.rerun()
            else:
                log_action(st.session_state["user_email"],f"Failed login attempt for '{email}'","warning")
                st.error("Please enter both email and password.")

def register_page():
    st.title("Register for Eduflex")
    log_action(st.session_state["user_email"],"Register page accessed", "info")

    lottie_animation = load_lottie_animation("animations//login animation.json")
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
                        log_action(st.session_state["user_email"],"Register page accessed", "info")
                        st.success("Registration successful! Please log in.")
                        st.session_state["active_page"] = "login"  
                    else:
                        log_action(st.session_state["user_email"],f"Registration failed for '{email}'", "warning")
                        st.error("Registration failed. Try again.")
                else:
                    log_action(st.session_state["user_email"],"Password mismatch during registration", "warning")
                    st.error("Passwords do not match.")
            else:
                log_action(st.session_state["user_email"],"Incomplete registration attempt", "warning")
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
    query_params = st.query_params
    feature = query_params.get("feature", "Welcome")  

    chosen = option_menu(
        menu_title=None,
        options=["Welcome", "Learn", "Skill Test", "Road Map", "Get Materials", "Compiler", "PDF Chat"],
        icons=["snow3", "bi-book-half", "clipboard2-data", "clipboard2-check", "book", "code", "book"],
        default_index=["Welcome", "Learn", "Skill Test", "Road Map", "Get Materials", "Compiler", "PDF Chat"].index(feature),
        orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "blue"}}
    )

    st.query_params["feature"] = chosen

    log_action(st.session_state["user_email"], f"Navigation selected: '{chosen}'", "info")

    if chosen == "Welcome":
        app()
        HOME()
    elif chosen == "Learn":
        LEARN(username=st.session_state["user_email"])
    elif chosen == "Skill Test":
        TEST(st.session_state["user_email"])
    elif chosen == "Road Map":
        ROADMAP(st.session_state["user_email"])
    elif chosen == "Get Materials":
        GET_MATERIAL(st.session_state["user_email"])
    elif chosen == "Compiler":
        code_with_ai(st.session_state["user_email"])
    elif chosen == "PDF Chat":
        PDF_CHAT(st.session_state["user_email"])


def page_routing():
    if st.session_state["active_page"] == "login":
        login_page()
    elif st.session_state["active_page"] == "register":
        register_page()
    elif st.session_state["logged_in"]:
        main_app()

top_navigation()
page_routing()

