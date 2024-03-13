#!/usr/bin/python3
""" Starts a Flash Web Application.
"""

from flask import Flask

app = Flask(__name__)

# Define the route for the root URL '/'
@app.route('/airbnb-onepage/', strict_slashes=False)
def hello_hbnb():
    """ Displays 'Hello HBNB! """
    return 'Hello HBNB!'

if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
