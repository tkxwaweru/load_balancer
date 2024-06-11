"""
load_balancer.py

Responsible for implementing the load balancers functionalities and endpoints
"""

import os
import requests
from consistent_hash_map import ConsistentHashMap
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize active servers from environment variable
active_servers = os.getenv("ACTIVE_SERVERS", "1 2 3").split()
num_slots = 1024  # Increase the number of slots for better distribution
consistent_hash_map = ConsistentHashMap(len(active_servers), num_slots)

# Dictionary to store requests mapped to servers
requests_mapping = {server: [] for server in active_servers}


# /rep endpoint - display active replicas
@app.route("/rep", methods=["GET"])
def get_replicas():
    return (
        jsonify(
            {
                "message": {"N": len(active_servers), "replicas": active_servers},
                "status": "successful",
            }
        ),
        200,
    )


# /add endpoint - add a server replica
@app.route("/add", methods=["POST"])
def add_server():
    data = request.json
    n = int(data.get("n", 0))
    hostnames = data.get("hostnames", [])
    if n <= 0 or len(hostnames) != n:
        return (
            jsonify(
                {"message": "<Error> Invalid request payload", "status": "failure"}
            ),
            400,
        )

    # Check if the new hostnames follow the naming convention
    for hostname in hostnames:
        if not hostname.isdigit():
            return (
                jsonify(
                    {
                        "message": f"<Error> Invalid hostname: {hostname}",
                        "status": "failure",
                    }
                ),
                400,
            )

    print(f"Adding {n} servers: {hostnames}")
    for hostname in hostnames:
        active_servers.append(hostname)
        requests_mapping[hostname] = []  # Initialize request mapping for new server
        consistent_hash_map.add_server(hostname)  # Update the consistent hash map

    print(f"Current active servers: {active_servers}")
    return (
        jsonify(
            {
                "message": {"N": len(active_servers), "replicas": active_servers},
                "status": "successful",
            }
        ),
        200,
    )


# /rm endpoint - remove a replica
@app.route("/rm", methods=["DELETE"])
def remove_server():
    data = request.json
    n = int(data.get("n", 0))
    hostnames = data.get("hostnames", [])
    if n <= 0 or len(hostnames) != n:
        return (
            jsonify(
                {"message": "<Error> Invalid request payload", "status": "failure"}
            ),
            400,
        )

    for hostname in hostnames:
        if hostname in active_servers:
            active_servers.remove(hostname)
            requests_mapping.pop(
                hostname, None
            )  # Remove request mapping for removed server

    consistent_hash_map.remove_server(hostname)  # Update existing consistent hash map
    return (
        jsonify(
            {
                "message": {"N": len(active_servers), "replicas": active_servers},
                "status": "successful",
            }
        ),
        200,
    )


@app.route("/<path:path>", methods=["GET"])
def route_request(path):
    server_id = consistent_hash_map.get_server(path)
    try:
        response = requests.get(f"http://server{server_id}:5000/home")
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify({"message": response.json(), "status": "successful"}), 200
    except requests.RequestException as e:
        return (
            jsonify({"message": f"<Error> {str(e)}", "status": "failure"}),
            500,
        )


@app.route("/requests/<string:server_id>", methods=["GET"])
def get_requests_mapped_to_server(server_id):
    # Check if server_id exists in the requests_mapping dictionary
    if server_id in requests_mapping:
        return (
            jsonify(
                {
                    "requests": requests_mapping[server_id],
                    "status": "successful",
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"message": "Server ID not found", "status": "failure"}),
            404,
        )


# /request endpoint
@app.route("/request", methods=["GET"])
def handle_request():
    request_id = int(request.args.get("request_id"))
    server_id = consistent_hash_map.get_server(str(request_id))
    try:
        response = requests.get(f"http://server{server_id}:5000/home")
        response.raise_for_status()  # Raise an error for bad responses

        # Update the requests_mapping dictionary
        if server_id not in requests_mapping:
            requests_mapping[server_id] = []
        requests_mapping[server_id].append(request_id)

        return (
            jsonify(
                {
                    "response": {
                        "message": response.json()["message"],
                        "status": "Successful",
                    },
                    "server_id": server_id,
                }
            ),
            200,
        )
    except requests.RequestException as e:
        return (
            jsonify({"message": f"<Error> {str(e)}", "status": "failure"}),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
