# engine/helpers/whatsapp_helper.py
import urllib.parse

def get_whatsapp_url(phone_number, message):
    """
    Constructs a WhatsApp "Click to Chat" URL with validation.

    Args:
        phone_number (str): The phone number, including country code.
        message (str): The message to be pre-filled.

    Returns:s
        dict: A dictionary with response, action, and URL for the frontend.
    """
    # Remove any non-digit characters (+, -, (), etc.)
    cleaned_number = ''.join(filter(str.isdigit, phone_number))

    # --- NEW: Add a length check for better validation ---
    # We'll assume a valid number must have at least 10 digits (common for country code + number).
    if len(cleaned_number) < 10:
        return {
            "response": f"The phone number '{phone_number}' seems too short. Please provide a valid number including the country code.",
            "action": None,
            "url": None
        }

    # URL-encode the message to handle special characters and spaces
    encoded_message = urllib.parse.quote_plus(message)

    # Construct the wa.me URL
    url = f"https://wa.me/{cleaned_number}?text={encoded_message}"

    return {
        "response": f"Opening WhatsApp to send a message to {phone_number}. You'll need to press send.",
        "action": "open_url",
        "url": url
    }