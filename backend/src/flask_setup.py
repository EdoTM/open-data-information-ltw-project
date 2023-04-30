from flask import Flask
from flask_cors import CORS
import os
from Crypto.PublicKey import RSA

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(32)

app.config["RSA_PRIV_KEY"] = RSA.generate(1024)


CORS(app, supports_credentials=True, origins=["*"])
