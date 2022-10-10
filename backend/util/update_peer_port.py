import os.path, requests
from backend.config import PEER_HELPER_PORT

DOCKERFILE_LINE_NUMBER = 7
CONFIG_LINE_NUMBER = 3

def get_port():
    selected_port = requests.get(f'http://localhost:{PEER_HELPER_PORT}/peer/port')
    return selected_port.json()

def project_base_dir():
    project_base_dir = os.path.dirname(__file__).split("backend/util")[0]
    return project_base_dir

def read_file_lines(filename):
    file_to_read = open(filename, "r")
    lines_list = file_to_read.readlines()
    file_to_read.close()
    return lines_list

def write_to_file(updated_lines_list, filename):
    update_file = open(filename, "w")
    update_file.writelines(updated_lines_list)
    update_file.close()

def update_file(replacement_line, filename, line_number):
    lines_list = read_file_lines(filename)
    lines_list[line_number] = replacement_line
    print(lines_list)
    write_to_file(lines_list, filename)


def main():
    peer_port = get_port()
    dockerfile = project_base_dir() + 'dockerfiles/Dockerfile.server.peer'
    app_file = project_base_dir() + 'backend/config.py'

    update_file(f'EXPOSE {peer_port}\n', dockerfile, DOCKERFILE_LINE_NUMBER-1)
    update_file(f'PEER_PORT = {peer_port}\n', app_file, CONFIG_LINE_NUMBER-1)

if __name__ == '__main__':
    main()