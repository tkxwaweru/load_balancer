import os
import random
from flask import Flask, jsonify, request
import math

# Define the ConsistentHashMap class
class ConsistentHashMap:
    def _init_(self, num_servers, num_slots):
        self.num_slots = num_slots
        self.servers = []
        self.virtual_servers = {}
        self.num_virtual_servers = math.floor(math.log2(num_slots))
        for i in range(num_servers):
            self.add_server(i)

    def hash_request(self, request_id):
        return (request_id + 2 ** request_id + 17) % self.num_slots

    def hash_server(self, server_id, virtual_id):
        return (server_id + virtual_id + 2 ** virtual_id + 25) % self.num_slots

    def add_server(self, server_id):
        for virtual_id in range(self.num_virtual_servers):
            slot = self.hash_server(server_id, virtual_id)
            while slot in self.virtual_servers:
                slot = (slot + 1) % self.num_slots  # Linear probing
            self.virtual_servers[slot] = (server_id, virtual_id)
            self.servers.append(slot)
        self.servers.sort()

    def remove_server(self, server_id):
        slots_to_remove = [slot for slot, (sid, vid) in self.virtual_servers.items() if sid == server_id]
        for slot in slots_to_remove:
            del self.virtual_servers[slot]
            self.servers.remove(slot)

    def get_server(self, request_id):
        request_hash = self.hash_request(request_id)
        for slot in self.servers:
            if slot >= request_hash:
                return self.virtual_servers[slot][0]
        return self.virtual_servers[self.servers[0]][0]

# Initialize the Flask application
app = Flask(_name_)

# Initialize the consistent hash map with the active servers
active_servers = list(map(int, os.getenv('ACTIVE_SERVERS', '1 2 3').split()))
num_slots = 512
consistent_hash_map = ConsistentHashMap(len(active_servers), num_slots)


@app.route("/home", methods=["GET"])
def home():
    server_id = random.choice(active_servers)
    return (
        jsonify({"message": f"Hello from Server: {server_id}", "status": "Successful"}),
        200,
    )

@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return "", 200

@app.route("/request", methods=["GET"])
def handle_request():
    request_id = int(request.args.get('request_id'))
    server_id = consistent_hash_map.get_server(request_id)
    return jsonify({'request_id': request_id, 'server_id': server_id})

if _name_ == "_main_":
    # Run the Flask app on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)