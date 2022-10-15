import requests
from requests.exceptions import HTTPError
from quick_start.parser import Parser
from backend.util.update_peer_port import project_base_dir, write_to_file, read_from_file

# python3 -m quick_start.start_peers -p=1 -a=http://localhost:5001/peer/port

script_description = 'Quick start script to obtain peer port and update files.'
commands = {
    'peers': ['p', 'Specify number of peer instances to create. Will default to 1 if no input given', int, True],
    'helper_address': ['a', 'Specify the address for communications with port_selector (backend.config)', str, True]
}
starter = Parser(script_description, commands)
peers = starter.args.peers
req_add = starter.args.helper_address
base_dir = f'{project_base_dir()}/'

for i in range(peers):
    peer_port = None
    client_port = None

    try:
        response = requests.get(req_add)
        response.raise_for_status()
        peer_port = response.json()['peer_port']
        client_port = peer_port - 2000

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    # update frontend, dockerfile
    # adjusts ports in backend.config
    server_config_file = f'{base_dir}backend/config.py'
    config = read_from_file(server_config_file)
    config[2] = f'TRUSTED_CLIENT_PORT = {client_port}\n'
    config[3] = f'PEER_PORT = {peer_port}\n'
    write_to_file(config, server_config_file)

    # update peer.yaml
    peer_compose = f'{base_dir}peer.yaml'
    compose = read_from_file(peer_compose)
    compose[7] = f'      - {peer_port}:{peer_port}\n'
    compose[18] = f'      - {client_port}:{client_port}'
    compose[28] = f'    command: ["./wait-for-it.sh", "api:{peer_port}", "--timeout=10", "--strict", "--", "npm", "run", "start" ]\n'
    write_to_file(compose, peer_compose)

    # update frontend, dockerfiles
    single_line_updates = [
        [f'    "start": "export PORT={client_port} react-scripts start",\n', f'{base_dir}/frontend/package.json', 19],
        [f'EXPOSE {client_port}\n', f'{base_dir}/dockerfiles/Dockerfile.client', 8], 
        [f'EXPOSE {peer_port}\n', f'{base_dir}/dockerfiles/Dockerfile.server.peer', 7], 
    ]

    for update in single_line_updates:
        write_to_file(update[0], update[1], update[2])

# run docker compose