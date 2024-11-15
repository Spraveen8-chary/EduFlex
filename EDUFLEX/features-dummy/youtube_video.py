import os
import streamlit as st
from streamlit_clickable_images import clickable_images
from apikey import YOUTUBE_API_KEY
import requests
import urllib.parse
from pytube import YouTube
from pytube.exceptions import PytubeError

def LEARN():
    st.title("Course Recommender")
    API_KEY = YOUTUBE_API_KEY

    @st.cache_data
    # Function to search for videos based on a query
    def search_videos(query, max_results=6):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={urllib.parse.quote(query)}&type=video&key={API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Debug: Check if there are items in the response
        if 'items' not in data:
            st.error("No videos found. Please try a different search query.")
            return []

        video_data = []
        for item in data['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_data.append({
                "title": title,
                "thumbnail": thumbnail_url,
                "url": video_url
            })
        return video_data

    # Ask user for search query
    c1, c2 = st.columns(2)
    with c1:
        query = st.text_input("What do you want to learn?")
    with c2:
        level = st.selectbox("Choose your learning level", ["Beginner", "Intermediate", "Advanced"])

    full_query = f"{query} {level} full course"
    videos = search_videos(full_query)

    if not videos:
        return  # Stop if no videos were found

    titles = [video["title"] for video in videos]
    thumbnails = [video["thumbnail"] for video in videos]
    links = [video["url"] for video in videos]

    # Display clickable images with thumbnails
    if query:
        selected_video = clickable_images(
            thumbnails,
            titles=titles,
            div_style={
                "height": "500px",
                "display": "grid",
                "grid-template-columns": "repeat(2, 1fr)",
                "justify-content": "center",
                "align-items": "center",
                "flex-wrap": "nowrap",
                "overflow-y": "auto"
            },
            img_style={"margin": "10px", "height": "250px"}
        )

        # Show selected video details and embed video
        if selected_video is not None and selected_video > -1:
            video_url = links[selected_video]
            video_title = titles[selected_video]

            st.markdown(f"### {video_title}")
            st.video(video_url)

# Run the app
if __name__ == "__main__":
    LEARN()
