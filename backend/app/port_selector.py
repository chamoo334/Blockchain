import os, random, atexit
from flask import Flask, jsonify, request
from backend.config import APP_PORT, PEER_HELPER_PORT
from backend.scripts.update_peer_port import project_base_dir, write_to_file

PORT = PEER_HELPER_PORT
RANGE_START = PORT + 1
RANGE_END = PORT + 1000

PORTS_IN_USE = [APP_PORT, PORT]

def random_port():
    return random.randint(RANGE_START, RANGE_END)

app = Flask(__name__)

@app.route('/')
def route_default():
    return 'Here to help select a peer port'

@app.route('/peer/port')
def route_peer_port():
    PEER_PORT = random_port()

    while PEER_PORT in PORTS_IN_USE:
        PEER_PORT = random_port()

    PORTS_IN_USE.append(PEER_PORT)

    return jsonify({ 'peer_port': PEER_PORT})

@app.route('/remove/port', methods=['POST'])
def route_remove_port():
    remove_port = request.get_json()['available_port']
    PORTS_IN_USE.remove(remove_port)
    return 'Removed port'

@atexit.register
def remove_self_backup_ports_in_use():
    PORTS_IN_USE.remove(PORT)

    ports_backup = project_base_dir() + 'backend/scripts/ports_list_backup.txt'
    ports_string_list = [f'{port}\n' for port in PORTS_IN_USE]
    write_to_file(ports_string_list, ports_backup)

def signal_handler(sig, frame):
    remove_self_backup_ports_in_use()
    os._exit(0)


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')