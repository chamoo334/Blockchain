import os

def project_base_dir():
    cwd = os.getcwd()
    return cwd

def write_to_file(items_to_write, write_file):
    data_file = open(write_file, 'w')
    data_file.writelines(items_to_write)
    data_file.close()

def read_from_file(read_file):
    data_file = open(read_file, 'r')
    data = list(data_file)
    data_file.close()
    return data

if __name__ == '__main__':
    project_base_dir()