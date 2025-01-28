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

# Function to interact with FastAPI to search for products
def search_products(query, min_price, max_price):
    response = requests.post(f"{FASTAPI_URL}/search-products", json={"query": query, "min_price": min_price, "max_price": max_price})
    return response.json().get('products', [])

# Function to interact with FastAPI to get Gemini response
def get_gemini_response(query):
    response = requests.get(f"{FASTAPI_URL}/get-response", params={"query": query})
    return response.json().get('response', "Sorry, I couldn't process that.")

# Main Streamlit interface
def main():
    st.set_page_config(page_title="Customer Chatbot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
    
    # Add Title and Subtitle
    st.title("AI-Powered Customer Chatbot")
    st.subheader("Ask questions or get product recommendations")

    # Sidebar for interaction options
    with st.sidebar:
        st.header("Interaction Options")
        interaction_type = st.radio("Choose Input Mode", ("Text Input", "Voice Input"))
        output_type = st.radio("Choose Output Mode", ("Text Output", "Voice Output"))
        min_price = st.number_input("Minimum Price", min_value=0, value=0)
        max_price = st.number_input("Maximum Price", min_value=0, value=100000)

    # Non-product conversation section
    non_product_conversation = st.button("Non-product Conversation")
    if non_product_conversation:
        st.write("You are now in a normal customer interaction mode. Ask anything!")
        
        # Input for user query
        user_query = listen() if interaction_type == "Voice Input" else st.text_input("Ask me a question or query:", key="user_input")
        
        # Use FastAPI for normal interaction (Gemini)
        if user_query:
            response = get_gemini_response(user_query)
            st.write(response)
            st.session_state['history'].append(f"Bot: {response}")
            if output_type == "Voice Output":
                speak_text(response)

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

    # User input section based on chosen interaction mode
    if interaction_type == "Text Input":
        user_query = st.text_input("Ask me a question or query:")

    if interaction_type == "Voice Input" and st.button("Speak"):
        user_query = listen()

    # Button for fetching product details from SerpAPI
    if st.button("ANSWER"):
        if user_query:
            products = search_products(user_query, min_price, max_price)
            filtered_products = []
            for product in products:
                # Only add products with rating > 4.5
                rating = float(product.get("rating", 0))
                if rating > 4.5:
                    title = product.get("title", "No title")
                    price = product.get("price", "No price")
                    link = product.get("link", "No link")
                    filtered_products.append({
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "link": link
                    })

            if filtered_products:
                formatted_info = ""
                for product in filtered_products:
                    formatted_info += f"**Product:** {product['title']}\n"
                    formatted_info += f"**Price:** {product['price']}\n"
                    formatted_info += f"**Rating:** {product['rating']}\n"
                    formatted_info += f"**Link:** {product['link']}\n\n"
                st.write(formatted_info)
                st.session_state['history'].append(f"Bot: {formatted_info}")
                if output_type == "Voice Output":
                    speak_text(formatted_info)  # Voice output
            else:
                st.warning("No products with a rating higher than 4.5 found.")
        else:
            st.warning("Please enter a product name to search.")

if __name__ == "__main__":
    main()
