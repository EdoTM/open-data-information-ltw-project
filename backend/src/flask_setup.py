from flask import Flask
from flask_cors import CORS
import os
from Crypto.PublicKey import RSA

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(32)

rsa_priv_key = RSA.generate(2048)
app.config["RSA_PRIV_KEY"] = rsa_priv_key


CORS(app, supports_credentials=True, origins=["http://localhost:*"])
