import streamlit as st
from dotenv import load_dotenv
load_dotenv() ##loads all the environment variables
import os
import google.generativeai as genai 

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a youtube video summarizer. You will be taking the transcript text and 
summarizing the entire video and provividing the important summary in points within 200-250 words
Please provide the summary of the text given : """

##getting the data from youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text:
            transcript+=" " + i["text"]

        return transcript

    except Exception as e:
        raise e

##getting the summary based on prompt from google gemini
def generate_gemini_content(transcript_text, prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text


st.title("Youtube Transcript to Detailed Notes Converter")
Youtube_link=st.text_input("Enter the Youtube video link: ")

if Youtube_link:
    video_id=Youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(Youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
