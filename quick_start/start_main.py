from quick_start.parser import Parser
from backend.util.update_peer_port import project_base_dir, write_to_file, read_from_file


base_dir = f'{project_base_dir()}/'
server_config_file = f'{base_dir}/backend/config.py'
main_compose = f'{base_dir}/main.yaml'

def update_main(app_port, helper_port):
    client_port = app_port - 2000

    # adjusts ports in backend.config
    config = read_from_file(server_config_file)
    config[0] = f'APP_PORT = {app_port}\n'
    config[1] = f'PEER_HELPER_PORT = {helper_port}\n'
    config[2] = f'TRUSTED_CLIENT_PORT = {client_port}\n'
    write_to_file(config, server_config_file)

    # update main.yaml
    compose = read_from_file(main_compose)
    compose[8] = f'      - {helper_port}:{helper_port}\n'
    compose[14] = f'      - {app_port}:{app_port}\n'
    compose[19] = f'    command: ["./wait-for-it.sh", "helper:{helper_port}", "--timeout=10", "--strict", "--", "python", "-m", "backend.app"]\n'
    compose[25] = f'      - {client_port}:{client_port}\n'
    compose[28] = f'    command: ["./wait-for-it.sh", "api:{app_port}", "--timeout=10", "--strict", "--", "npm", "run", "start" ]\n'
    write_to_file(compose, main_compose)

    # adjust ports in frontend, dockerfiles
    single_line_updates = [
        [f'    "start": "export PORT={client_port} react-scripts start",\n', f'{base_dir}/frontend/package.json', 19],
        [f'EXPOSE {client_port}\n', f'{base_dir}/dockerfiles/Dockerfile.client', 8], 
        [f'EXPOSE {app_port}\n', f'{base_dir}/dockerfiles/Dockerfile.server.main', 6], 
        [f'EXPOSE {helper_port}\n', f'{base_dir}/dockerfiles/Dockerfile.server.helper', 5],
    ]

    for update in single_line_updates:
        write_to_file(update[0], update[1], update[2])

def update_run_main(app_port, helper_port):
    update_main(app_port, helper_port)
    # run docker compose


if __name__ == '__main__':
    script_description = 'Quick start script to update and run port_selector and primary api (default: 5000) and client (default: 3000).'
    commands = {
        'app_port': ['a', 'Specify the port for the main backend port. Will default to 5000 if no input given.', int],
        'helper_port': ['p', 'Specify the port for the port selector to run on. Will default to 5001 if no input given', int]
    }
    starter = Parser(script_description, commands)
    app_port = 5000 if starter.args.app_start_port is None else starter.args.app_port
    helper_port = 5001 if starter.args.helper_port is None else starter.args.helper_port
    update_run_main(app_port, helper_port)