# engine/helpers/system_helper.py

import os
import subprocess
import datetime

# --- A SAFER WAY TO OPEN APPLICATIONS ON WINDOWS ---
# We create a "whitelist" of allowed applications and their commands.
# This prevents users from running malicious commands like "open format c:".
# You can easily add more Windows applications and file paths here.
# Use forward slashes '/' or double backslashes '\\' for paths.
APP_MAP = {
    'notepad': 'notepad.exe',
    'calculator': 'calc.exe',
    'command prompt': 'cmd.exe',
    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'vs code': 'C:/Users/YourUsername/AppData/Local/Programs/Microsoft VS Code/Code.exe' # IMPORTANT: Change 'YourUsername'
}

def open_app(command):
    """
    Opens a whitelisted application on Windows.
    """
    # Extract the app name from a command like "open vs code"
    app_name = command.replace("open", "").strip().lower()
    
    if app_name not in APP_MAP:
        return {"response": f"Sorry, I don't know how to open '{app_name}'. It's not in my list of known applications."}

    app_path = APP_MAP[app_name]

    try:
        # os.startfile is the safest and easiest way to open files or apps on Windows.
        os.startfile(app_path)
        return {"response": f"Opening {app_name}."}

    except FileNotFoundError:
        return {"response": f"Sorry, I couldn't find '{app_name}' at the path '{app_path}'. Please check the path in system_helper.py."}
    except Exception as e:
        print(f"Error opening application: {e}")
        return {"response": f"Sorry, a system error occurred while trying to open {app_name}."}





def handle_date(command):
    today = datetime.date.today().strftime("%B %d, %Y")
    return {"response": f"Today's date is {today}."}