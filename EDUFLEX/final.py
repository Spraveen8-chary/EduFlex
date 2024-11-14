import streamlit as st
import cv2
from streamlit_option_menu import option_menu
from features.apikeys import geminiai_api_key
apikey = geminiai_api_key
import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie

# '''New Features....'''
from features.home import HOME, load_local_lottie
from features.certificate_generation import generate_certificate
from features.course import LEARN
from features.test import TEST
from features.roadmap import ROADMAP
from features.materials import GET_MATERIAL

st.set_page_config("EDUFLEX",page_icon="🔖",layout="wide")

logo = cv2.imread("animations\\logo.jpg")

def app():
    #st.image(logo, use_column_width=True)

    with st.sidebar:

        #st.image(logo, use_column_width=True)
        lottie_animation2 = load_local_lottie("animations\\logo_animation.json")
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


genai.configure(api_key=apikey)

chosen = option_menu(
    menu_title=None,
    options = ["Welcome","Learn","Skill Test","Road Map","Get Materials"],
    icons = ["snow3","bi-book-half","clipboard2-data","clipboard2-check","book"],
    default_index=0,
    orientation="horizontal")

if chosen == "Welcome":
    HOME()

if chosen == "Learn":
    LEARN()

if chosen == "Skill Test":
    TEST()

if chosen == "Road Map":
    ROADMAP()

if chosen=="Get Materials":
    GET_MATERIAL()