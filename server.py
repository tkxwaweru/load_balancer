'''
For our server we shall employ python's flask library for server creation and configuration.
'''
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get the server ID from the environment variable
server_id = int(os.environ.get('SERVER_ID', 1))

@app.route('/home', methods=['GET'])
def home():
    return jsonify({"message": f"Hello from Server: {server_id}", "status": "Successful"}), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)