import os, random, atexit, signal
from datetime import datetime
# from backend.util.update_peer_port import project_base_dir, write_to_file

def project_base_dir():
    cwd = os.getcwd()
    print(cwd)

def write_to_file(items_to_write, write_file):
    print('write_to_file')

if __name__ == '__main__':
    project_base_dir()