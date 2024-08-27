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
from firebase_admin import firestore

cred = credentials.Certificate("flashcrd-firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#client = OpenAI()


@app.route('/health-check')
def health_check():
    logger.info("in health check")
    return jsonify({"message": "Hello World!"})


@app.route('/get-flashcards')
def get_flashcards():
    logger.info('in get flashcards')
    flashcard_set_name = request.args.get('flashcardSetName')
    logger.info('dat: ' + str(flashcard_set_name))
    doc_ref = db.collection('flashcards').document(flashcard_set_name)
    # Fetch the document
    doc = doc_ref.get()
    if doc.exists:
        logger.info(f'Document data: {doc.to_dict()}')
        return jsonify(doc.to_dict())
    else:
        logger.info(f'No document found with ID:')
    return None


# oAI_prompt = """
# You are a flashcard creator, you take in text and create multiple flashcards from it. Make sure to create exactly 10 flashcards.
# Both front and back should be one sentence long.
# You should return in the following JSON format:
# {
#   "flashcards":[
#     {
#       "front": "Front of the card",
#       "back": "Back of the card"
#     }
#   ]
# }
# """




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)