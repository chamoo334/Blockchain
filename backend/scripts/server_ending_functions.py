import os.path, requests
from backend.config import PEER_HELPER_PORT

def remove_port_listing(port):
    update = requests.post(f'http://localhost:{PEER_HELPER_PORT}/peer/port', json={'available_port': port})
    print(update.status_code)

def initial_check(port):
    print(f'Terminating server on port {port}')

def copy_ports_in_use():
    # TODO: copy ports to file for use later
    pass