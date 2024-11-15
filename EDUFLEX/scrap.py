import streamlit as st

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Function to set the page
def set_page(page):
    st.session_state.current_page = page

# Custom CSS styling
st.markdown(
    """
    <style>
    /* Navbar container */
    .navbar {
        background-color: #4a4a8e;  /* Violet background color */
        padding: 30px 450px;
        border-radius: 8px;
        # text-align: center;
        margin-bottom: -20px;
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-left: -90px;
    }
     div.stButton > button{
        background-color: #fff !important;  /* White button background */
        color: #4a4a8e !important;  /* Violet text color */
        border: none !important;
        padding: 30px 0px !important;
        font-size: 16px !important;
        border-radius: 5px !important;
        cursor: pointer !important;
        width: 50px !important;
        margin-top:-90px !important;
    }

    /* Hover effect for buttons */
    div.stButton > button:hover {
        background-color: #e0e0e0 !important;  /* Light gray on hover */
    }

    /* Focus effect */
    div.stButton > button:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navbar with buttons using Streamlit columns
st.markdown("<div class='navbar'>", unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

# Buttons for navigation
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

# Page content based on the current page
st.write(f"### {st.session_state.current_page}")

if st.session_state.current_page == "Home":
    st.write("Welcome to the Home Page")
elif st.session_state.current_page == "Learn":
    st.write("Welcome to the Learn Page")
elif st.session_state.current_page == "Test":
    st.write("Welcome to the Test Page")
elif st.session_state.current_page == "Road Map":
    st.write("Welcome to the Road Map Page")
elif st.session_state.current_page == "Get Materials":
    st.write("Welcome to the Get Materials Page")
elif st.session_state.current_page == "Compiler":
    st.write("Welcome to the Compiler Page")
elif st.session_state.current_page == "PDF Chat":
    st.write("Welcome to the PDF Chat Page")
elif st.session_state.current_page == "Search Engine":
    st.write("Welcome to the Search Engine Page")
