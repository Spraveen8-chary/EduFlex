import os
import streamlit as st
from features.logger import log_action
from features.apikeys import GEMINI_API_KEY
import google.generativeai as genai
from helpers.toast_messages import get_random_toast
from helpers.quiz import get_quiz_data
from helpers.quiz_utils import string_to_list, get_randomized_options
from features.apikeys import GEMINI_API_KEY

def TEST(username = ''):
    genai.configure(api_key=GEMINI_API_KEY)
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
        log_action(username, "Quiz Form Submitted!")
        print(skill_topic, skill_level, skill, number_of_questions)
        with st.spinner("Crafting your quiz...🤓"):
            if submitted:
                # video_id = extract_video_id_from_url(YOUTUBE_URL)
                # quiz_data_str = get_quiz_data(skill_topic, skill_level, skill_topic, number_of_questions)
                quiz_data_str = get_quiz_data(skill=skill, level= skill_level, topic=skill_topic, number_of_questions=number_of_questions)
                print("Quiz Data (Raw):", quiz_data_str)
                cleaned_quiz_data_str = quiz_data_str.replace("```python", "").replace("```", "").strip()
                st.session_state.quiz_data_list = string_to_list(cleaned_quiz_data_str)

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

                                # os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY
                                
                                # text = get_video_text(YOUTUBE_URL)
                                quiz_data = " ".join(map(str, st.session_state.quiz_data_list))

                                prompt_template = f"""This is the question that is generated with the inputs of {skill} the user want to take test 
                                                    in the particular {skill_topic} with the his level of understanding at {skill_level} level.These are the 
                                                    questions that are generated {quiz_data} with the inputs the user have given.User have chosen the option {ro[ua]}.
                                                    But the correct option is {ca}.I want you to write a short and crisp explation why is {ca} is the correct option since you are an expert in {skill}."""
                                model = genai.GenerativeModel("gemini-1.5-pro")
                                response = model.generate_content(
                                    prompt_template + skill + skill_level + skill_topic + q[0] + quiz_data + ro[
                                        ua] + ca)
                                st.info(response.text)
                    if score:
                        log_action(username, f"Quiz Details => Programming Language : '{skill}'  =>  Topic : '{skill_topic}'  =>  Level : '{skill_level}'  =>  No. of Questions => '{number_of_questions}'  => Correct : '{score}'  =>  Total Question : {len(st.session_state.quiz_data_list)}  =>  ")    
                    else:
                        log_action(username, f"Quiz Details => Programming Language : '{skill}'  =>  Topic : '{skill_topic}'  =>  Level : '{skill_level}'  =>  No. of Questions => '{number_of_questions}'  => Correct : 'Quiz Not Started'  =>  Total Question : {len(st.session_state.quiz_data_list)}  =>  ")    
