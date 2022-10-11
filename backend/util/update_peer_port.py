import os, random, atexit, signal
from datetime import datetime
from flask import Flask, jsonify, request
from backend.config import PEER_HELPER_PORT
from backend.util.update_peer_port import project_base_dir, write_to_file

PORT = PEER_HELPER_PORT
RANGE_START = PORT + 1
RANGE_END = RANGE_START + 1000

PORTS_IN_USE = [PORT]

def random_port():
    return random.randint(RANGE_START, RANGE_END)

def update_ports_add(new_port):
    PORTS_IN_USE.append(new_port)

def update_ports_remove(old_port):
    PORTS_IN_USE.remove(old_port)

app = Flask(__name__)

@app.route('/')
def route_default():
    return 'Here to help select a peer port'

@app.route('/peer/port')
def route_peer_port():
    PEER_PORT = random_port()

    while PEER_PORT in PORTS_IN_USE:
        PEER_PORT = random_port()

    update_ports_add(PEER_PORT)

    return jsonify({ 'peer_port': PEER_PORT})

@app.route('/remove/port', methods=['POST'])
def route_remove_port():
    remove_port = request.get_json()['available_port']
    update_ports_remove(remove_port)
    return 'Removed port'

@app.route('/update/server/port', methods=['POST'])
def route_add_port():
    server_port = request.get_json()['server_port']
    if server_port in PORTS_IN_USE:
        update_ports_remove(server_port)
    else:
        update_ports_add(server_port)
    return 'Updated server_port'

@app.route('/get/ports')
def route_get_ports():
    return jsonify(ports = PORTS_IN_USE)

@atexit.register
def remove_self_backup_ports_in_use():
    update_ports_remove(PORT)
    ports_backup = project_base_dir() + f'backend/backups/ports-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt'
    ports_string_list = [f'{port}\n' for port in PORTS_IN_USE]
    write_to_file(ports_string_list, ports_backup)

#TODO: switch to sys.exit for cleaner
def signal_handler(sig, frame):
    remove_self_backup_ports_in_use()
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')