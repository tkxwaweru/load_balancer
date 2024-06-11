"""
Server.py:

Responsible for initializing the servers using the flask python library
"""

import os
from flask import Flask, jsonify, request
from consistent_hash_map import ConsistentHashMap

# Initialize the Flask application
app = Flask(__name__)

# Initialize the consistent hash map with the active servers
server_id = int(os.getenv("SERVER_ID", "1"))
num_slots = 512


# /home endpoint
@app.route("/home", methods=["GET"])
def home():
    return (
        jsonify({"message": f"Hello from Server: {server_id}", "status": "Successful"}),
        200,
    )


# heartbeat endpoint
@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return "", 200


if __name__ == "__main__":
    # Run the Flask app on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
