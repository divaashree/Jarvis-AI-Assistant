# app.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from engine.commands import process_command

# Initialize the Flask application
# We configure it to serve files from the 'www' directory.
app = Flask(__name__,
            static_folder="www/assets",          # The folder for static files (CSS, JS, images)
            template_folder="www")        # The folder for HTML template files (index.html)

# Enable CORS (Cross-Origin Resource Sharing)
# This is crucial for allowing the frontend (browser) to communicate with this backend server.
CORS(app)


@app.route('/')
def index():
    """
    This function serves the main user interface.
    When a user visits the root URL (e.g., http://localhost:5000),
    Flask will look for 'index.html' in the 'template_folder' and send it.
    """
    return render_template('index.html')


@app.route('/process-command', methods=['POST'])
def handle_command():
    """
    This is the main API endpoint for processing commands.
    The JavaScript frontend will send POST requests to this URL.
    """
    try:
        # Get the JSON data that was sent from the JavaScript frontend.
        data = request.get_json()
        
        # Extract the command string from the JSON data.
        # We use .get() to avoid an error if 'command' is not present.
        command = data.get('command')

        if not command:
            # If no command was sent, return a bad request error.
            return jsonify({"error": "No command provided."}), 400

        # This is where the magic happens:
        # We call your main 'process_command' function from commands.py
        result = process_command(command)
        
        # 'result' is the dictionary returned by your command processor.
        # We convert it to a JSON response to send back to the browser.
        return jsonify(result)

    except Exception as e:
        # A robust error handler for any unexpected issues on the server.
        # It's good practice to log the error for debugging purposes.
        print(f"An error occurred in handle_command: {e}")
        # Return a generic error message to the user.
        return jsonify({"response": "Sorry, an internal server error occurred."}), 500


if __name__ == '__main__':
    # This block runs the server when you execute 'python app.py' in your terminal.
    # host='0.0.0.0' makes the server accessible from other devices on your local network.
    # port=5000 is the standard port for local Flask development.
    # debug=True enables auto-reloading when you save code changes and provides detailed error pages.
    app.run(host='0.0.0.0', port=5000, debug=True)