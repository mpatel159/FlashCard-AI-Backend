import logging
#from openai import OpenAI
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import requests
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("flashcrd-firebase.json")
firebase_admin.initialize_app(cred)


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#client = OpenAI()


@app.route('/health-check')
def health_check():
    logger.info("in health check")
    return jsonify({"message": "Hello World!"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)