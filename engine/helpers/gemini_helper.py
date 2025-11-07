# engine/helpers/gemini_helper.py

import google.generativeai as genai
from engine.config import GEMINI_API_KEY

def get_gemini_response(query):
    """
    Sends a query to the Gemini API and gets a conversational response.
    
    Args:
        query (str): The user's question or command.
        
    Returns:
        str: The text response from Gemini, or an error message.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        return "Gemini API key is not configured. Please add it to engine/config.py."
    
    try:
        # Configure the API with your key
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Create the model
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # 1.5-flash is fast and powerful
        
        # Send the query and get the response
        response = model.generate_content(query)
        
        # Return the text part of the response
        return response.text
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I'm having trouble connecting to my creative brain right now."