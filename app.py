
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_ollama.chat_models import ChatOllama

# Initialize the chat model
model = ChatOllama(model="llama3.2:1b")




# Define prompt for the AI model
prompt = """You are a YouTube video summarizer. You will take the transcript text and summarize 
the entire video, providing the important summary in points within 250 words.
The transcript text will be appended below. Please provide the summary of the text given here."""

# Function to extract transcript from YouTube video
def extracted_transcript_detail(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[-1]
        print(video_id)
        transcripted_text = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine transcript into a single string
        transcript = " ".join([i["text"] for i in transcripted_text])
        return transcript
    except Exception as e:
        return str(e)

# Function to generate summary using AI model
def generate_content(transcript_text, subject):
    
    response = model.invoke(f"{prompt}\n{transcript_text}")
    return response

# Streamlit UI
st.title('YouTube Transcript Summarizer')

# Input field for YouTube video URL
youtube_link = st.text_input('Enter YouTube video link:')

# Display video thumbnail if URL is entered
if youtube_link:
    video_id = youtube_link.split("=")[-1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

# Button to generate transcript and summary
if st.button('Get Detailed Notes'):
    transcripted_text = extracted_transcript_detail(youtube_link)

    if transcripted_text:
        summary = generate_content(transcripted_text, "YouTube Video Summary")

        st.markdown("### Detailed Notes:")
        st.write(summary.content)
