# Ai_Powered_Call_Centre_Intelligence_Suryaraman-infosys-springboard-
# AI-Powered Customer Chatbot

This project is an AI-powered customer chatbot that helps users interact via text and voice input/output. The chatbot uses Google Gemini for generating responses and SerpAPI for searching products. It is built using FastAPI for the backend and Streamlit for the frontend.

## Features

- **Text and Voice Input**: Users can interact with the chatbot through text or voice input.
- **Text and Voice Output**: The chatbot provides responses either in text or by voice.
- **Product Search**: Search products using SerpAPI, with the option to filter by price range.
- **Normal Conversation Mode**: Users can ask any non-product-related questions, and the chatbot will respond using Google Gemini.
- **Real-time Speech-to-Text and Text-to-Speech**: Uses Google Text-to-Speech (gTTS) for voice output and SpeechRecognition for voice input.

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Product Search**: SerpAPI
- **AI Model**: Google Gemini (Generative AI)
- **Speech-to-Text**: SpeechRecognition
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Audio Playback**: Pygame

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/customer-chatbot.git
    ```

2. Navigate to the project directory:
    ```bash
    cd customer-chatbot
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory with the following keys:
        ```env
        SERPAPI_KEY=your_serpapi_key
        GOOGLE_API_KEY=your_google_api_key
        ```

5. Run the FastAPI backend:
    ```bash
    uvicorn main:app --reload
    ```

6. Run the Streamlit frontend:
    ```bash
    streamlit run app.py
    ```

## License

This project is licensed under the MIT License.
