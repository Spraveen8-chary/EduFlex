import streamlit as st
from streamlit_ace import st_ace
import requests
import sys
import io
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

def code_with_ai():
    # st.set_page_config(page_title="Code With AI", page_icon=":guardsman:", layout="wide", initial_sidebar_state="expanded")

    LANGUAGES = {
        "python": "3.9.7",  
        "javascript": "node-14.17.0",  
        "java": "15.0.2",  
        "c_cpp": "10.2.0",  
        "bash": "5.1.0",  
        "csharp": "9.0.0", 
        "html": "latest", 
        "css": "latest",
        "ruby": "3.0.0",  
        "sql": "5.7",  
        "swift": "5.7.1", 
        "typescript": "4.4.3",
        "go": "1.17.0", 
        "php": "7.4.3",  
        "kotlin": "1.5.0",  
        "rust": "1.56.0", 
        "r": "4.1.2", 
        "matlab": "R2021b", 
        "perl": "5.32",  
        "scala": "2.13.6",  
        "haskell": "8.10.4", 
    }

    POPULAR_LANGUAGES = [
        "python", "javascript", "java", "c_cpp", "csharp", "html", "css", "ruby", "sql", "swift", 
        "typescript", "go", "php", "kotlin", "rust", "r", "matlab", "bash", "perl", "scala", "haskell"
    ]

    THEMES = [
        "monokai", "github", "tomorrow", "twilight", "solarized_dark", "solarized_light", "terminal", "dracula"
    ]

    KEYBINDINGS = [
        "vscode", "emacs", "sublime", "vim"
    ]

    if "code" not in st.session_state:
        st.session_state.code = "" 

    st.sidebar.header("Editor Settings")
    language = st.sidebar.selectbox("Language", options=list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index("python"))
    theme = st.sidebar.selectbox("Theme", options=THEMES, index=THEMES.index("monokai"))
    keybinding = st.sidebar.selectbox("Keybinding", options=KEYBINDINGS, index=KEYBINDINGS.index("vscode"))
    font_size = st.sidebar.slider("Font Size", min_value=10, max_value=24, value=16)

    editor_col, output_col = st.columns([3, 1]) 

    with editor_col:
        st.markdown("### Code Editor")
        code = st_ace(
            placeholder="Write your code here", 
            language=language, 
            theme=theme, 
            keybinding=keybinding, 
            font_size=font_size, 
            tab_size=4, 
            height=450,  
            value=st.session_state.code if st.session_state.code else "print('Hello from Python')" if language == "python" else "", 
            
        )
        st.session_state.code = code


    with output_col:
        st.markdown("### Output")

        if st.button("Run Code"):
            if language=='python':
                output = io.StringIO()
                sys.stdout = output 
                
                try:
                    exec(st.session_state.code)
                    sys.stdout = sys.__stdout__  
                    st.text(output.getvalue())  
                except Exception as e:
                    sys.stdout = sys.__stdout__  
                    st.error(f"Error in code execution: {e}")
            else:
                payload = {
                    "language": language,
                    "version": LANGUAGES[language],  
                    "files": [
                        {
                            "name": "main." + ("txt"), 
                            "content": code
                        }
                    ],
                    "args": [], 
                }

                try:
                    response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)
                    result = response.json()

                    if response.status_code == 200:
                        st.text(result['run']['output'])  
                    else:
                        st.error(f"Error executing code: {result}")
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("Code With AI🤖"):
        
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',  
            tools='code_execution'
        )
        response = model.generate_content((
            f"""Assume yourself as a good programmer who's is expert in multiple programming languages. 
            Now I'll give some inputs like user writen code, programming language. based on it 1st generate the output then explain his code and generate your code in same programming language along with output.
            USER_CODE = f```{code} ```
            LANGUAGE = f{language}...            
            """
        ))
        if response.text:
            st.markdown(response.text)
                
        else:
            st.warning("Error")
