import random
from flask import Flask, jsonify
from backend.config import APP_PORT, PEER_HELPER_PORT

PORTS_IN_USE = [APP_PORT, PEER_HELPER_PORT]

app = Flask(__name__)

@app.route('/')
def route_default():
    return 'Here to help select a peer port'

@app.route('/peer/port')
def route_peer_port():
    RANGE_START = PEER_HELPER_PORT + 1
    RANGE_END = PEER_HELPER_PORT + 1000
    PEER_PORT = random.randint(RANGE_START, RANGE_END)

    while PEER_PORT in PORTS_IN_USE:
        PEER_PORT = random.randint(5002, 6000)

    PORTS_IN_USE.append(PEER_PORT)

    return jsonify({ 'peer_port': PEER_PORT})

print(PORTS_IN_USE)
app.run(port=PEER_HELPER_PORT, host='0.0.0.0')