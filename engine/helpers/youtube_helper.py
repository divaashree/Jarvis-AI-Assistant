# engine/helpers/youtube_helper.py

def play_on_youtube(topic):
    """
    Finds and plays a video on YouTube using the pywhatkit library.

    Args:
        topic (str): The song, video, or topic to search for.

    Returns:
        str: A response message for Jarvis to speak.
    """
    try:

        import pywhatkit
        # This is the magic line. It will find and play the video.
        pywhatkit.playonyt(topic)
        
        # Return a success message
        return f"Now playing '{topic}' on YouTube."
        
    except Exception as e:
        # Handle potential errors, like no internet connection.
        print(f"Error using pywhatkit: {e}")
        return "Sorry, I couldn't play the video. Please check your internet connection."
    

"""
import urllib.parse

def get_youtube_url(topic):
   """ """
    Constructs a YouTube search URL for the given topic.
    Returns a dictionary with instructions for the frontend.
    """ """
    if not topic:
        return {
            "response": "Please tell me what you want to play on YouTube.",
            "action": None,
            "url": None
        }

    # URL-encode the topic to handle spaces and special characters, making it safe for a URL
    query = urllib.parse.quote_plus(topic)
    url = f"https://www.youtube.com/results?search_query={query}"
    
    # This dictionary is the "plan" we send back to the frontend
    return {
        "response": f"Opening YouTube to search for '{topic}'.",
        "action": "open_url",  # A special instruction for the frontend
        "url": url
    }
"""

