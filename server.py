import os
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Define the list of active server IDs
active_servers = [1, 2, 3]

# Generate a random server ID from the list of active servers
server_id = random.choice(active_servers)


@app.route("/home", methods=["GET"])
def home():
    return (
        jsonify({"message": f"Hello from Server: {server_id}", "status": "Successful"}),
        200,
    )


@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return "", 200


if __name__ == "__main__":
    # Run the Flask app on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)