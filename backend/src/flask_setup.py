from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(32)
CORS(app, supports_credentials=True, origins=["http://localhost:*"])

