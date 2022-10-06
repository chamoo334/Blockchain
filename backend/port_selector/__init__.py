import random
from flask import Flask, jsonify, request
from backend.config import APP_PORT, PEER_HELPER_PORT
from backend.scripts.server_ending_functions import initial_check, copy_ports_in_use

PORT = PEER_HELPER_PORT
PORTS_IN_USE = [APP_PORT, PORT]

app = Flask(__name__)

@app.route('/')
def route_default():
    return 'Here to help select a peer port'

@app.route('/peer/port')
def route_peer_port():
    RANGE_START = PORT + 1
    RANGE_END = PORT + 1000
    PEER_PORT = random.randint(RANGE_START, RANGE_END)

    while PEER_PORT in PORTS_IN_USE:
        PEER_PORT = random.randint(5002, 6000)

    PORTS_IN_USE.append(PEER_PORT)

    return jsonify({ 'peer_port': PEER_PORT})

@app.route('/remove/port', methods=['POST'])
def route_remove_port():
    remove_port = request.get_json()
    print(remove_port)

@app.route('/shutdown', methods=['POST'])
def shutdown_port_selector():
    print('Shutdown context hit with POST!')
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('The function is unavailable!')
    else:
        initial_check()
        shutdown()

if __name__ == '__main__':
    print(PORTS_IN_USE)
    app.run(port=PORT, host='0.0.0.0')