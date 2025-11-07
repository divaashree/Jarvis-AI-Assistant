# engine/skills.py

# Import all the necessary helpers from your existing project
from engine.helpers.weather_helper import get_weather
from engine.helpers.news_helper import get_top_headlines, find_country_code
from engine.helpers.wikipedia_helper import search_wikipedia
from engine.helpers.youtube_helper import play_on_youtube  #get_youtube_url,
from engine.helpers.email_helper import send_email_directly
from engine.helpers.whatsapp_helper import get_whatsapp_url
# The system helpers now return a dictionary directly, which is great.
from engine.helpers.system_helper import open_app, handle_date

# --- COUNTRY CODE MAP ---
# Maps common country names to their 2-letter ISO codes for the News API.
# You can easily add more countries to this list.


def handle_youtube_open(command):
    """Handles the command 'open youtube'."""
    return {
        "response": "Opening YouTube...",
        "action": "open_url",
        "url": "https://www.youtube.com"
    }

"""
def handle_youtube_play(command):
   """ """Handles playing a specific video on YouTube.""""""
    # We extract the topic more cleanly here
    topic = command.replace("play", "").replace("on youtube", "").strip()
    if not topic:
        return {"response": "What would you like me to play on YouTube?"}
    return get_youtube_url(topic)
"""

def handle_youtube_play(command):
    """Handles playing any video on YouTube using pywhatkit."""
    topic = command.replace("play", "").replace("on youtube", "").strip()
    
    if not topic:
        return {"response": "What would you like me to play on YouTube?"}
        
    # Call the new helper and get the response message
    response_message = play_on_youtube(topic)
    
    # NOTE: pywhatkit opens the browser itself, so there is no 'action' or 'url'.
    # We just return the response message for Jarvis to speak.
    return {"response": response_message}

def handle_wikipedia_search(command):
    """Handles general Wikipedia searches."""
    # Define trigger words to be removed for a cleaner topic extraction
    triggers = ["wikipedia", "who is", "what is", "explain", "define", "tell me about"]
    topic = command
    for trigger in triggers:
        topic = topic.replace(trigger, "")
    topic = topic.strip()
    
    if not topic:
        return {"response": "What topic would you like to search on Wikipedia?"}
        
    # A simple easter egg
    if "joke" in command:
        return {"response": "Why don't scientists trust atoms? Because they make up everything!"}
        
    result = search_wikipedia(topic)
    return {"response": result}

# In engine/skills.py

def handle_whatsapp_message(command):
    """
    Handles sending a WhatsApp message.
    This version safely parses the command and provides helpful errors.
    """
    # Extracts everything after the trigger phrase (e.g., "whatsapp")
    args_str = command.partition("whatsapp")[-1].strip() or command.partition("send a message to")[-1].strip()

    # --- NEW: Safely check for the separator before splitting ---
    if ';' not in args_str:
        return {
            "response": " Please use the format: 'whatsapp [phone number]; [message]' to send a message."
        }
    
    # Now that we know a semicolon exists, we can safely split the string
    try:
        phone_number, message = args_str.split(';', 1)
        # Check if either part is empty after splitting
        if not phone_number.strip() or not message.strip():
            raise ValueError("Empty phone number or message")
            
        return get_whatsapp_url(phone_number.strip(), message.strip())
        
    except ValueError:
        # This will catch cases like "whatsapp ;;" or "whatsapp num;"
        return {"response": "Please use the format: 'whatsapp [phone number]; [message]'."}

def handle_email(command):
    """Handles sending an email directly from the backend."""
    try:
        # Extract arguments: "send email [recipient]; [subject]; [body]"
        args_str = command.replace("send email", "").strip()
        recipient, subject, body = args_str.split(';', 2)
        
        # Call the new direct sending function
        response_message = send_email_directly(recipient.strip(), subject.strip(), body.strip())
        
        # Return the result for Jarvis to speak
        return {"response": response_message}
        
    except (ValueError, IndexError):
        return {"response": "Please use the format: 'send email [recipient]; [subject]; [body]'"}

def handle_weather(command):
    """Handles weather requests."""
    city = command.replace("weather in", "").replace("weather", "").strip()
    if city:
        weather_report = get_weather(city)
        return {"response": weather_report}
    else:
        return {"response": "Please specify a city, like 'weather in London'."}
    
def handle_news(command):
    """
    Handles fetching news by finding the country and calling the helper.
    """
    # 1. Call our new function to find the country code from the command.
    country_code = find_country_code(command)
    
    # 2. Call the main helper, passing the code we just found.
    news_report = get_top_headlines(country=country_code)
    
    # 3. Return the result.
    return {"response": news_report}

    
def handle_exit(command):
    """Handles exit commands."""
    return {"response": "Goodbye! Have a great day."}

def jarvis(command):

    return{"response" : "I was built by D.I.V.A.K.A.R... "}



# --- THE COMMAND REGISTRY (The "Phone Book") ---
# We map trigger keywords to the functions that handle them.
# The order is important: more specific commands should come before general ones.
COMMAND_REGISTRY = {
    # Trigger tuple : Function
    ("play", "on youtube"): handle_youtube_play,
    ("open youtube",): handle_youtube_open,
    ("whatsapp", "send a message"): handle_whatsapp_message,
    ("send email",): handle_email,
    ("weather", "forecast"): handle_weather,
    ("news", "headlines", "report"): handle_news,
    ("wikipedia", "who is"): handle_wikipedia_search,
    ("exit", "stop", "bye", "goodbye"): handle_exit,
     # System Commands 
    ("open",): open_app, 
    ("date", "what is today"): handle_date,
    ("who built you","who developed you","who is your boss"):jarvis,
 
}