# EDUFLEX: Adaptive Learning Platform 

## Overview
This adaptive learning platform recommends educational courses based on user-specified subjects and levels of understanding (beginner, intermediate, advanced). It utilizes various features, including course recommendations through the YouTube API, note-taking, site-blocking for focused learning, Pomodoro timers for time management, interactive Q&A with chatbots trained on video transcriptions, skill assessments with feedback, personalized learning roadmaps, and certifications upon completion.

## Features
- **Course Recommendation System**: Based on user-specified subjects and skill levels, fetches and ranks courses from YouTube.
- **Note-taking System**: Integrated notes feature to assist users in capturing information during learning.
- **Site-Blocking Extension**: Blocks distracting websites during study sessions.
- **Pomodoro Timer**: Implements the Pomodoro technique for better time management during learning.
- **Interactive Q&A with Videos**: Chatbots answer user queries based on video transcriptions.
- **Skill Testing and Feedback**: Personalized skill assessments with immediate feedback to track progress.
- **Learning Roadmap Generator**: Generates personalized roadmaps to guide users through their learning journey.
- **PDF Notes & Certification**: Provides supplementary notes and certifications upon course completion.
- **Multi Compiler**: Which can run upto 20 programming languages.

## System Design
- **Course Recommendation Algorithm**: Uses data collection, user profiling, and a recommendation engine to provide accurate course suggestions.
- **Chat with Video**: Utilizes Retrieval Augmented Generation (RAG) with a vector database and semantic search to enhance video-based interactions.
- **Skill Assessment**: Generates skill tests dynamically and provides real-time feedback.

## Methodology
- **Data Collection**: From user inputs and YouTube API.
- **Recommendation Engine**: Personalizes recommendations based on user interests and preferences.
- **Skill Testing & Feedback**: Provides immediate, detailed feedback to enhance learning outcomes.

## Installation

1. Clone the repository.
```
https://github.com/Spraveen8-chary/EduFlex.git
```
2. Install required dependencies.
```
pip install -r requirements.txt
```
3. Set up YouTube API credentials.
4. Run the platform.
```
streamlit run --server.port 8000 app.py
```

## Output Video

[screen-capture (2).webm](https://github.com/user-attachments/assets/b917fed9-fd50-4970-a669-464b5c820d34)
