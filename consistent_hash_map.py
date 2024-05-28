import hashlib

class ConsistentHashMap:
    def __init__(self, num_servers, num_slots):
        self.num_slots = num_slots
        self.servers = []
        self.virtual_servers = {}
        self.num_virtual_servers = 100  # Increase the number of virtual nodes
        for i in range(1, num_servers + 1):  # Start from 1 to match Docker service names
            self.add_server(str(i))  # Ensure server IDs are strings

    def hash_request(self, request_id):
        hashed_value = int(hashlib.md5(str(request_id).encode()).hexdigest(), 16) % self.num_slots
        print(f"Hashed value for request {request_id}: {hashed_value}")
        return hashed_value

    def hash_server(self, server_id, virtual_id):
        hashed_value = int(hashlib.md5(f"{server_id}-{virtual_id}".encode()).hexdigest(), 16) % self.num_slots
        print(f"Hashed value for server {server_id} with virtual id {virtual_id}: {hashed_value}")
        return hashed_value

    def add_server(self, server_id):
        print(f"Adding server {server_id}...")
        for virtual_id in range(self.num_virtual_servers):
            slot = self.hash_server(server_id, virtual_id)
            probing_attempts = 0
            while slot in self.virtual_servers:
                probing_attempts += 1
                slot = (slot + (2 * virtual_id) + 1) % self.num_slots  # Quadratic probing
                if probing_attempts > self.num_slots:
                    print(f"Error: Too many probing attempts for server {server_id} virtual_id {virtual_id}. Exiting.")
                    return
            self.virtual_servers[slot] = (server_id, virtual_id)
            self.servers.append(slot)
            print(f"Assigned virtual server {virtual_id} of server {server_id} to slot {slot}")
        self.servers.sort()
        print(f"Server {server_id} added. Current servers: {self.servers}")
        print(f"Current virtual servers mapping: {self.virtual_servers}")

    def remove_server(self, server_id):
        print(f"Removing server {server_id}...")
        slots_to_remove = [
            slot
            for slot, (sid, vid) in self.virtual_servers.items()
            if sid == server_id
        ]
        for slot in slots_to_remove:
            del self.virtual_servers[slot]
            self.servers.remove(slot)
        print(f"Server {server_id} removed. Current servers: {self.servers}")
        print(f"Current virtual servers mapping: {self.virtual_servers}")

    def get_server(self, request_id):
        request_hash = self.hash_request(request_id)
        print(f"Hashed request {request_id}: {request_hash}")
        for slot in self.servers:
            if slot >= request_hash:
                selected_server = self.virtual_servers[slot][0]
                print(f"Request {request_id} assigned to server {selected_server}")
                return selected_server
        selected_server = self.virtual_servers[self.servers[0]][0]
        print(f"Request {request_id} assigned to server {selected_server}")
        return selected_server
