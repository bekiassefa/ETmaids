from flask import Flask

# Create the Flask app instance
app = Flask(__name__)

# Import and register the routes
from app import routes