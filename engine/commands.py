# engine/commands.py

# We only need to import our new registry
from engine.skills import COMMAND_REGISTRY
from engine.helpers.gemini_helper import get_gemini_response

def process_command(command):
    """
    Processes a command by first checking the local command registry,
    and if no match is found, sends it to the Gemini API for a
    conversational response.
    """
    command = command.lower().strip()

    if not command:
        return {"response": "I didn't hear anything. Please try again."}

    # --- LAYER 1: The "Reflex" System ---
    # First, try to find a specific, pre-programmed command.
    for triggers, function in COMMAND_REGISTRY.items():
        if any(trigger in command for trigger in triggers):
            # If a local command is matched, execute it and we're done.
            return function(command)

    # --- LAYER 2: The "Cloud Brain" ---
    # If the loop finishes and no local command was found,
    # seamlessly send the query to Gemini for a general response.
    gemini_answer = get_gemini_response(command)
    
    return {"response": gemini_answer}