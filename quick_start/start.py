from quick_start.parser import Parser

script_description = 'Blockchain initialization script. Requires argument for number of peers.'
commands = {'peers': ['p', 'Specify number of peer instances to create. Will default to 1 if no input given', int]}
starter = Parser(script_description, commands)
total_peers = 1 if starter.args.peers is None else starter.args.peers


#  start port_selector

# start main api backend and frontend

# start up peer instances


def test():
    print(total_peers)


if __name__ == '__main__':
    test()