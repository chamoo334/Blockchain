from quick_start.parser import Parser
from backend.util.update_peer_port import project_base_dir

script_description = 'Blockchain initialization script. Requires argument for number of peers.'
commands = {'peers': ['p', 'Specify number of peer instances to create. Will default to 1 if no input given', int]}
starter = Parser(script_description, commands)
starter.args.peers = 1 if starter.args.peers is None else starter.args.peers
base_dir = project_base_dir()
dockerfile_dir = f'{base_dir}/dockerfiles'

# start port_selector

# start main api backend and frontend

# start up peer instances


def main():
    print('peer: ', starter.args.peers)


if __name__ == '__main__':
    main()