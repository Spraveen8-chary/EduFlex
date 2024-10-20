import streamlit as st

# State variable to store current playback time
if "watched_time" not in st.session_state:
    st.session_state["watched_time"] = 0.0

def update_watched_time(time_delta):
  st.session_state["watched_time"] += time_delta

def on_playback_change():
  global video_element
  video_element = st.experimental_js("get_video_element")
  if video_element is not None:
      current_time = video_element.currentTime
      # Update watched time only if video is playing
      if video_element.paused is False:
          update_watched_time(current_time - st.session_state["watched_time"])
      st.session_state["watched_time"] = current_time

# Display the video
video_file = st.video("https://www.youtube.com/watch?v=EECUXqFrwbc")
video_element = None

# Listen for video playback events
on_playback_change()
st.on_event("video.playing", on_playback_change)
st.on_event("video.paused", on_playback_change)

# Display watched time
if video_element is not None:
  st.write(f"Watched Time: {st.session_state['watched_time']:.2f} seconds")
