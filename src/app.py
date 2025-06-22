import json
from typing import List

from flask import Flask, request

from conversation import Conversations
from common import logger

app = Flask(__name__)


conversations = Conversations()

scammers = []  # list of phone numbers of scammers

@app.route("/scammers", methods=["GET"])
def get_scammers() -> str:
    return json.dumps(scammers)


@app.route("/scammers", methods=["DELETE"])
def delete_scammer():
    phone = request.get_json()["phone"]

    logger.debug("Deleting phone: " + phone)
    scammers.remove(phone)


@app.route("/check", methods=["POST"])
def check_phone() -> str:
    """
    Checks if the phone is in the list of scammers.
    Returns True if the phone is in the list of scammers, False otherwise.
    """

    phone = request.get_json().get("phone")

    logger.debug("Checking phone : " + phone)
    logger.debug(scammers)

    return json.dumps(phone in scammers)


@app.route("/analyze", methods=["POST"])
def analyze() -> List[str]:
    """
    Analyzes the phrase of the caller.
    Holds the information about the whole conversation based on the phone number of the caller.
    Returns the list of scam phrases in the conversation so far.
    If there are scam phrases, saves the phone number of the caller in the list of the scammers.
    """

    data = request.get_json()
    phone = data.get("phone")
    phrase = data.get("phrase")

    scam_phrases = conversations.analyze(phone, phrase)
    if len(scam_phrases) > 0:
        scammers.append(phone)

    return scam_phrases


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
