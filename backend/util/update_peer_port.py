import os

def project_base_dir():
    cwd = os.getcwd()
    return cwd

def write_to_file(items_to_write, write_file, line_num=None):
    if line_num is not None:
        data = read_from_file(write_file)
        data[line_num] = items_to_write
        items_to_write = data

    
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