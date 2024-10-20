import streamlit as st
import os
import google.generativeai as genai
from apikey import geminiai_api_key

apikey = geminiai_api_key

os.environ['GOOGLE_API_KEY'] = geminiai_api_key

genai.configure(api_key=apikey)

st.title("Daily Course Planner")


st.text_input("Please tell us your name")

col1, col2 = st.columns(2)

with col1:
    course = st.text_input("Which course do you want to learn")

with col2:
    learning_level  = st.selectbox("Choose your level of learning",["Beginner","Intermediate","Advanced"])

col3, col4 = st.columns(2)

with col3:
    no_of_hours = st.number_input("Choose number of learning hours per day",value = 1,placeholder="Choose here")
with col4:
    no_of_days = st.number_input("How many days you want to learn the skill",value=1,placeholder="Choose here")

target_level = st.selectbox("To which level do you want to reach at the end of the preparation",["Intermediate","Advanced"])

no_of_days = str(no_of_days)
no_of_hours = str(no_of_hours)

submit = st.button("Submit")

prompt_template = f'''You are course a lecture in the course.{course}I am you student who want to learn the course that you teach.
                        I am at this {learning_level}.I want to learn the course in {no_of_days} days by spending {no_of_hours} hours daily.
                        At the end of the preparation I need to reach {target_level}.As a lecturer in  the {course} I want a daily plan 
                        to follow to learn that course.Give me the plan according to the inputs that I have provided to reach the {target_level}.
                        Tell me where I have to start at the start of the day and the topics that I have to cover in the day and at what timings.
                        At the end of the day I want to revise the topics that  I have learnt at the end of the day so please add the revision time and the 
                        topics to recall. Start the plan with a motivational quote so that I can have a positive attitude while learning.Add the timings in which
                        to complete the topic.I cannot spend all {no_of_hours} hours at once so divide them in the day at each part of the day.
                        Ret
                        Output Format :
                        DAY_1 : 
                        9-10  : Topics to Cover
                        10-11 : Topics to cover
                        ""
                        ""
                        '''
model = genai.GenerativeModel("gemini-pro")
response = model.generate_content(prompt_template+course+learning_level+no_of_hours+no_of_days+target_level)

if submit:
    st.markdown(response.text)


