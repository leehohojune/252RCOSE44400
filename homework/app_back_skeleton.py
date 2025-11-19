from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Path to stored message file
DATA_PATH = "/data/message.txt"


def read_message():
    """
    TODO: 
    - If DATA_PATH exists, read and return the text inside
    - If it doesn't exist, return an empty string
    """
    pass


def write_message(msg: str):
    """
    TODO:
    - Open DATA_PATH
    - Write msg to the file
    """
    pass


@app.route("/api/message", methods=["GET"])
def get_message():
    """
    TODO:
    - Call read_message()
    - Return { "message": <stored message> } as JSON
    """
    pass


@app.route("/api/message", methods=["POST"])
def update_message():
    """
    TODO:
    - Get JSON from request
    - Extract the field "message"
    - Call write_message() to save it
    - Return { "status": "ok" }
    """
    pass


# v1 has no /api/health endpoint
# (Students add this in v2)

# v2 TODO:
# - Modify write_message() or update_message() to include a timestamp
#   Format: "<message> (updated at YYYY-MM-DD HH:MM:SS)"
#
# - Add new endpoint /api/health that returns:
#   { "status": "healthy" }


if __name__ == "__main__":
    # Do not change the host or port
    app.run(host="0.0.0.0", port=5001)
