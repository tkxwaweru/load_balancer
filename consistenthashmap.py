#defining the class and initializing attributes
import math

class ConsistentHashMap:
    def __init__(self, num_servers, num_slots):
        self.num_slots = num_slots
        self.servers = []
        self.virtual_servers = {}
        self.num_virtual_servers = math.floor(math.log2(num_slots))
        for i in range(num_servers):
            self.add_server(i)

#implement the hash function
    def hash_request(self, request_id):
        return (request_id + 2 ** request_id + 17) % self.num_slots

    def hash_server(self, server_id, virtual_id):
        return (server_id + virtual_id + 2 ** virtual_id + 25) % self.num_slots

#adding servers to the hash map
    def add_server(self, server_id):
        for virtual_id in range(self.num_virtual_servers):
            slot = self.hash_server(server_id, virtual_id)
            while slot in self.virtual_servers:
                slot = (slot + 1) % self.num_slots  # Linear probing
            self.virtual_servers[slot] = (server_id, virtual_id)
            self.servers.append(slot)
        self.servers.sort()

#a method to remove servers from the hash map
    def remove_server(self, server_id):
        slots_to_remove = [slot for slot, (sid, vid) in self.virtual_servers.items() if sid == server_id]
        for slot in slots_to_remove:
            del self.virtual_servers[slot]
            self.servers.remove(slot)

#method to find appropriate server for a given request
    def get_server(self, request_id):
        request_hash = self.hash_request(request_id)
        for slot in self.servers:
            if slot >= request_hash:
                return self.virtual_servers[slot][0]
        return self.virtual_servers[self.servers[0]][0]

# Example usage
if __name__ == '__main__':
    num_servers = 3
    num_slots = 512

    consistent_hash_map = ConsistentHashMap(num_servers, num_slots)

    # Adding a new server (with ID 4)
    consistent_hash_map.add_server(4)

    # Getting the server for a specific request
    request_id = 132574
    server_id = consistent_hash_map.get_server(request_id)
    print(f'Request {request_id} is mapped to server {server_id}')