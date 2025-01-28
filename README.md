# Ai_Powered_Call_Centre_Intelligence_Suryaraman-infosys-springboard-
# AI-Powered Customer Chatbot

This project is an AI-powered customer chatbot that helps users interact via text and voice input/output. The chatbot uses Google Gemini for generating responses and SerpAPI for searching products, filtering them by ratings. It is built using FastAPI for the backend and Streamlit for the frontend.

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

## How to Use

1. Choose the input and output modes from the sidebar (text or voice).
2. For normal conversations, click the **Non-product Conversation** button, ask a question, and receive a response.
3. To search for products, enter a query, set the price range, and click **ANSWER**. Products with ratings greater than 4.5 will be displayed.
4. The chat history can be viewed by checking the **Show chat history** option.
5. Click the **Stop Conversation** button to clear the chat history.

## License

This project is licensed under the MIT License.
