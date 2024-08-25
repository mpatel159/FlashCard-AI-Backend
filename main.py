import logging
from openai import OpenAI
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("flashcrd-firebase.json")
firebase_admin.initialize_app(cred)


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#client = OpenAI()

# initialize firebase
db = firestore.client()


@app.route('/health-check')
def health_check():
    logger.info("in health check")
    return jsonify({"message": "Hello World!"})



oAI_prompt = """
You are a flashcard creator, you take in text and create multiple flashcards from it. Make sure to create exactly 10 flashcards.
Both front and back should be one sentence long.
You should return in the following JSON format:
{
  "flashcards":[
    {
      "front": "Front of the card",
      "back": "Back of the card"
    }
  ]
}
"""

@app.route('/flashcards' , methods=['POST'])
def generate_flashcards():
    logger.info("in AI endpoint")
    data = request.get_data(as_text=True)
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": oAI_prompt},
                {"role": "user", "content": data},
            ]
        )
    flashcards = json.loads(response.choices[0].message['content'])
        
    # Save flashcards to Firestore
    flashcards_ref = db.collection('flashcards').add(flashcards)

    return jsonify({"id": flashcards_ref[1].id, "flashcards": flashcards['flashcards']})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5123))
    app.run(host='0.0.0.0', port=port, debug=True)