# engine/helpers/wikipedia_helper.py

import wikipedia
import re  # Import the regular expression module for cleaning text
import requests.exceptions # To catch network errors

def search_wikipedia(query, sentences=2):
    """
    Searches Wikipedia for a given query and returns a cleaned-up summary.
    This version is optimized for text-to-speech by removing parentheses and citations.

    Args:
        query (str): The topic to search for.
        sentences (int): The number of sentences for the summary.

    Returns:
        str: A cleaned summary or an error message.
    """
    if not query:
        return "Please provide a topic to search on Wikipedia."

    try:
        # It's good practice to set the language, just in case.
        wikipedia.set_lang("en")
        
        # Get the summary from the Wikipedia API
        summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True, redirect=True)
        
        # --- THIS IS THE KEY IMPROVEMENT FOR VOICE ---
        # Use regular expressions to remove content in parentheses and square brackets
        cleaned_summary = re.sub(r'\(.*?\)|\[.*?\]', '', summary)
        # Replace multiple spaces that might have been created with a single space
        cleaned_summary = ' '.join(cleaned_summary.split())
        
        return cleaned_summary

    except wikipedia.exceptions.DisambiguationError as e:
        # Make the suggestion a bit more conversational
        options = ", ".join(e.options[:3])
        return f"That query is a bit broad. Did you mean one of these: {options}? Please try again with a more specific term."
    
    except wikipedia.exceptions.PageError:
        return f"My apologies, I couldn't find a Wikipedia page for '{query}'."

    except (requests.exceptions.RequestException, wikipedia.exceptions.WikipediaException) as network_err:
        # This handles when there's no internet or Wikipedia's servers are down.
        print(f"Wikipedia network error: {network_err}")
        return "Sorry, I'm having trouble connecting to Wikipedia at the moment. Please check your internet connection."

    except Exception as e:
        # Catch any other unexpected errors.
        print(f"An unexpected Wikipedia Helper error occurred: {e}")
        return "Sorry, an unexpected error occurred while I was searching Wikipedia."