from flask import Flask
from flask_cors import CORS
from routes import register_routes
from scheduler import start_scheduler

import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_URL", "*")}})

@app.route("/")
def home():
    return "Email Marketing Backend is running"

register_routes(app)

if __name__ == "__main__":
    # Start scheduler before starting Flask server
    # start_scheduler() # Initialize APScheduler
    # print("Scheduler started. Weekly campaign job is scheduled.")

    # Run the Flask app
    app.run(debug=False)  # Set debug=False in production

# Note: In production, consider using a WSGI server like Gunicorn or uWSGI instead of Flask's built-in server.
     