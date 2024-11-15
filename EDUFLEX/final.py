import streamlit as st
import cv2
from streamlit_option_menu import option_menu
import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie

# New Features....
from features.apikeys import GEMINIAI_API_KEY
apikey = GEMINIAI_API_KEY
from features.home import HOME, load_local_lottie
from features.certificate_generation import generate_certificate
from features.course import LEARN
from features.test import TEST
from features.roadmap import ROADMAP
from features.materials import GET_MATERIAL
from features.compiler import code_with_ai


st.set_page_config("EDUFLEX",page_icon="🔖",layout="wide")

logo = cv2.imread("animations\\logo.jpg")


def app():

    with st.sidebar:

        lottie_animation2 = load_local_lottie("animations\\logo_animation.json")
        st_lottie(lottie_animation2, key="logo", height=150, width=150)

        markdown_text = """
        - Had you course completed ? Get your certificate from :blue[Eduflex] Today👇👇.
        """
        st.markdown(markdown_text)

        # Get the student's name
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
    

genai.configure(api_key=apikey)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Function to set the page
def set_page(page):
    st.session_state.current_page = page

st.markdown("""
    <style>
    .navbar {
        background-color: #4a4a8e;  /* Adjust this color as desired */
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: -90px;
        
    }
    .navbar div.stButton > button {
        background-color: #fff;  /* White button background */
        color: #4a4a8e;  /* Violet text color */
        border: none;
        padding: 10px 30px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }
    .navbar div.stButton > button:hover {
        background-color: #e0e0e0;  /* Light gray on hover */
        color: #4a4a8e;
    }
    </style>
""", unsafe_allow_html=True)

# Display the navbar with custom buttons using st.button
with st.container():
    st.markdown("<div class='navbar'>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        if st.button("🏛 Home"):
            set_page("Home")
    with col2:
        if st.button("📝 Learn"):
            set_page("Learn")
    with col3:
        if st.button("✍🏻 Test"):
            set_page("Test")
    with col4:
        if st.button("🎯 Road Map"):
            set_page("Road Map")
    with col5:
        if st.button("📚 Get Materials"):
            set_page("Get Materials")
    with col6:
        if st.button("👨🏻‍💻 Compiler"):
            set_page("Compiler")
    with col7:
        if st.button("📖 PDF Chat"):
            set_page("PDF Chat")
    with col8:
        if st.button("🧐 Search Engine"):
            set_page("Search Engine")
    st.markdown("</div>", unsafe_allow_html=True)

# Display the title of the current page
# st.write(f"### {st.session_state.current_page}")

# Page content logic
if st.session_state.current_page == "Home":
    app()
    HOME()

elif st.session_state.current_page == "Learn":
    LEARN()

elif st.session_state.current_page == "Test":
    TEST()

elif st.session_state.current_page == "Road Map":
    ROADMAP()

elif st.session_state.current_page == "Get Materials":
    GET_MATERIAL()

elif st.session_state.current_page == "Compiler":
    code_with_ai()

elif st.session_state.current_page == "PDF Chat":
    HOME()

elif st.session_state.current_page == "Search Engine":
    HOME()