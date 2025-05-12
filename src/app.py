from typing import List

from flask import Flask, request

from conversation import Conversations

app = Flask(__name__)


conversations = Conversations()


@app.route("/analyze", methods=["POST"])
def home() -> List[str]:
    data = request.get_json()
    phone = data.get("phone")
    phrase = data.get("phrase")

    return conversations.analyze(phone, phrase)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
