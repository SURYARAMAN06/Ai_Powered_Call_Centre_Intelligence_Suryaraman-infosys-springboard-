from fastapi import FastAPI, Query
from pydantic import BaseModel
import google.generativeai as genai
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

# Load environment variables (for API keys)
load_dotenv()

# SerpAPI Key
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize FastAPI app
app = FastAPI()

# Configure Google Gemini (Generative AI)
genai.configure(api_key=GOOGLE_API_KEY)

# Define Product Search Query model
class ProductSearchQuery(BaseModel):
    query: str
    min_price: float = 0.0
    max_price: float = 100000.0

# Function to search products using SerpAPI
def search_amazon(query, min_price, max_price):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_KEY,
        "gl": "IN",  # Geolocation for India
        "hl": "en",  # Language set to English
    }

    # Add price filters
    if min_price:
        params["min_price"] = min_price
    if max_price:
        params["max_price"] = max_price

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get('shopping_results', [])

# Function to get response from Gemini
def get_gemini_response(input_text):
    if input_text:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text])
        return response.text if response else "No response generated."
    return "Sorry, I couldn't process that."

# Endpoint to fetch product details
@app.post("/search-products")
async def search_products(query: ProductSearchQuery):
    products = search_amazon(query.query, query.min_price, query.max_price)
    return {"products": products}

# Endpoint for Gemini model to generate response for user query
@app.get("/get-response")
async def get_response(query: str):
    response = get_gemini_response(query)
    return {"response": response}
