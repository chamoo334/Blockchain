import argparse


class Parser:
    """
    
    """
    def __init__(self, msg, commands):
        self.parser = argparse.ArgumentParser(description = msg)
        self.add_commands(commands)
        self.args = self.parser.parse_args()
    
    def add_commands(self, new_command):
        """
        Dictionary with list values [-e, help_msg, type] for each key command.
        Example: {'--peers': ['p', 'Specify number of peer instances to create', int, {'const': 1}]}
        """
        for key in new_command:
            short, command_msg, input_type = new_command[key][0:3]
            command_required = new_command[key][3] if len(new_command[key]) > 3 else False
            
            self.parser.add_argument(f'-{short}', 
                                     f'--{key}', 
                                     help=command_msg, 
                                     type=input_type, 
                                     required=command_required)
            

if __name__ == '__main__':
    test_values = {'peers': ['p', 'Specify number of peer instances to create', int]}
    test = Parser("Blockchain initialization script. Requires argument for number of peers.", test_values)
    print(test.args.peers)
    print('done')
    