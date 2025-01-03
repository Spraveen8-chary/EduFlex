import streamlit as st
from streamlit_ace import st_ace
import requests
import sys
import io
import google.generativeai as genai
from features.apikeys import GEMINIAI_API_KEY


def code_with_ai():
    st.markdown("Code With AI 🤖")

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
            if language == 'python':
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

    if st.button("Code With AI 🤖"):
        genai.configure(api_key=GEMINIAI_API_KEY)

        tool = {
            "function_declarations": [
                {
                    "name": "explain_code",
                    "description": "Explains the given code and provides insights and also generate the output for user writen code too.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"},
                            "language": {"type": "string"}
                        }
                    }
                }
            ]
        }

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                tools=tool
            )
            response = model.generate_content(
                f"""
                Assume you are an expert programmer. Here is the user-provided code:
                Code: {code}
                Language: {language}
                Please explain the code and provide suggestions for improvement.
                """
            )
            print(response)
            # if response.candidates:
            #     st.write(response.candidates)
                
            #     if response.candidates[0].content and response.candidates[0].content.parts:
            #         st.markdown(response.candidates[0].content.parts[0].text)
            #     else:
            #         st.warning("No valid content parts in the response.")
            # else:
            #     st.warning("No response candidates found.")

            if response.text:
                st.markdown(response.text)
            else:
                st.warning("No response from the AI model.")

        except Exception as e:
            st.error(f"Error using Generative AI: {e}")


if __name__ == "__main__":
    code_with_ai()
