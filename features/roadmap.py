import streamlit as st
from features.apikeys import GEMINIAI_API_KEY
import google.generativeai as genai
import os
from features.logger import log_action

def ROADMAP(username = ''):
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
        log_action(username, "Roadmap Details submitted!...")
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
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt_template)
            plan = response.text
            st.markdown(plan)
            log_action(username, f"RoadMap Generated For '{course}'")

            # Save button to save the plan to a text file
            st.download_button(
                label="Download plan as text",
                data=plan,
                file_name=f"{course}_{no_of_days}_day_plan.txt",
                mime="text/plain",
            )

