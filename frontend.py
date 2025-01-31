import streamlit as st
import speech_recognition as sr
import pygame
import gtts
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI server URL (make sure this is the correct URL if you're deploying)
FASTAPI_URL = "http://localhost:8000"

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Initialize recognizer for speech-to-text
recognizer = sr.Recognizer()

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to convert text to speech using gTTS and pygame
def speak_text(text):
    if os.path.exists("response.mp3"):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove("response.mp3")
    
    tts = gtts.gTTS(text)
    tts.save("response.mp3")
    
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

# Function to listen to voice input and convert it to text
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio)
            st.write(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
            return None

# Function to interact with FastAPI to handle both normal and product-related queries
def handle_query(query, min_price, max_price):
    response = requests.post(f"{FASTAPI_URL}/handle-query", json={"query": query, "min_price": min_price, "max_price": max_price})
    return response.json().get('response', "No response from the server.")

# Main Streamlit interface
def main():
    st.set_page_config(page_title="Customer Chatbot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
    
    # Add Title and Subtitle
    st.title("AI-Powered Customer Chatbot")
    st.subheader("Ask questions to get product recommendations")

    # Sidebar for interaction options
    with st.sidebar:
        st.header("Interaction Options")
        interaction_type = st.radio("Choose Input Mode", ("Text Input", "Voice Input"))
        output_type = st.radio("Choose Output Mode", ("Text Output", "Voice Output"))
        min_price = st.number_input("Minimum Price", min_value=0, value=0)
        max_price = st.number_input("Maximum Price", min_value=0, value=100000)

    # User input section based on chosen interaction mode
    user_query = listen() if interaction_type == "Voice Input" else st.text_input("Ask me a question or query:", key="user_input")

    # Button for handling both normal and product-related queries
    if st.button("ANSWER"):
        if user_query:
            response = handle_query(user_query, min_price, max_price)
            st.write(response)
            st.session_state['history'].append(f"Bot: {response}")
            if output_type == "Voice Output":
                speak_text(response)
        else:
            st.warning("Please enter a product name or a question.")

    # Stop button to end conversation immediately
    stop_button = st.button("Stop Conversation")
    if stop_button:
        st.write("Conversation stopped.")
        st.session_state['history'] = []

    # Display chat history checkbox
    if st.checkbox("Show chat history"):
        st.subheader("Chat History")
        for message in st.session_state['history']:
            st.write(message)

if __name__ == "__main__":
    main()
