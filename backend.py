from fastapi import FastAPI, Query
from pydantic import BaseModel
import google.generativeai as genai
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

# Load environment variables (for API keys)
load_dotenv()

# SerpAPI Key and GoogleAPTkey
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

    if min_price:
        params["min_price"] = min_price
    if max_price:
        params["max_price"] = max_price

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get('shopping_results', [])

# Function to get response from Gemini, for both normal and product-related queries
def get_gemini_response(query, products=None):
    if products:
        product_details = "\n".join([f"Product: {p['title']}, Price: {p['price']}, Link: {p['link']}" for p in products])
        input_text = f"User query: {query}\nHere are the product details:\n{product_details} and also provide suggestions"
    else:
        input_text = f"User query: {query}. Please answer the query."
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text])
    
    return response.text if response else "No response generated."

# Endpoint to handle both normal and product-related queries
@app.post("/handle-query")
async def handle_query(query: ProductSearchQuery):
    # Try to fetch products based on the query
    products = search_amazon(query.query, query.min_price, query.max_price)

    # If products are found, include them in the LLM response; otherwise, handle it as a normal conversation
    if products:
        response = get_gemini_response(query.query, products)
    else:
        response = get_gemini_response(query.query)
    
    return {"response": response}
