import os
import google.generativeai as genai
from features.apikeys import GEMINIAI_API_KEY
apikey = GEMINIAI_API_KEY
from youtube_transcript_api import YouTubeTranscriptApi

os.environ["GOOGLE_API_KEY"] = GEMINIAI_API_KEY

genai.configure(api_key=apikey)

def get_video_text(video_url):
    try:
        video_id = video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " +i['text']

        return transcript

    except Exception as e:
        raise e

def get_quiz_data(skill,level,topic,number_of_questions):
    prompt_template = f"""
    You are a helpful assistant programmed to generate questions based on the skill , level at which the user was, the particular topic the user needs. From the inputs that you have received, you're tasked with designing user inputed number of distinct questions. Each of these questions will be accompanied by 4 possible answers: one correct answer and two incorrect ones. 
    You have to create exactly {number_of_questions} for the user.
    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

    Your output should be shaped as follows:

    1. An outer list that contains 5 inner lists.
    2. Each inner list represents a set of question and answers, and contains exactly 5 strings in this order:
    - The generated question.
    - The correct answer.
    - The first incorrect answer.
    - The second incorrect answer.
    - The third incorrect answer

    Your output should mirror this structure:
    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2","Incorrect Answer 1.3"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2","Incorrect Answer 2.3"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.
    Skill : {skill}
    Level : {level}
    Topic : {topic}
    Number of questions : {number_of_questions} 
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    complete_prompt = prompt_template + skill + topic + level + str(number_of_questions)
    
    response = model.generate_content(complete_prompt)

    return  response.text