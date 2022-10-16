from quick_start.parser import Parser
from quick_start.start_main import update_run_main
from quick_start.start_peers import update_run_peers
from backend.util.update_peer_port import project_base_dir



def main(peers, app_port, helper_port, req_address):
    # start port_selector (5001) and main api (5000) backend and frontend (3000)
    update_run_main(app_port, helper_port)

    # start up peer instances (call port_selector and update files)
    update_run_peers(peers, req_address)


if __name__ == '__main__':
    script_description = 'Blockchain initialization script. Requires argument for number of peers.'
    commands = {
        'peers': ['p', 'Specify number of peer instances to create. Will default to 1 if no input given', int],
        'app_port': ['a', 'Specify the port for the main backend port. Will default to 5000 if no input given.', int],
        'helper_port': ['h', 'Specify the port for the port selector to run on. Will default to 5001 if no input given', int],
        'helper_address': ['a', 'Specify the address for communications with port_selector (backend.config)', str, True]
    }
    starter = Parser(script_description, commands)
    starter.args.peers = 1 if starter.args.peers is None else starter.args.peers
    starter.args.app_port = 5000 if starter.args.app_port is None else starter.args.app_port
    starter.args.helper_port = 5001 if starter.args.helper_port is None else starter.args.helper_port
    base_dir = project_base_dir()
    dockerfile_dir = f'{base_dir}/dockerfiles'
    main(starter.args.peers, starter.args.app_port, starter.args.helper_port, starter.args.helper_address)