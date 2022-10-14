from backend.scripts.parser import Parser

script_description = 'Blockchain initialization script. Requires argument for number of peers.'
commands = {'peers': ['p', 'Specify number of peer instances to create', int]}
starter = Parser(script_description, commands)
total_peers = 1 if starter.args.peers is not None else starter.args.peers


#  start port_selector

# start main api backend and frontend

# start up peer instances
