import subprocess

def dock_comp_up(up_file):
    subprocess.run(["docker", "compose", "up", "-f", up_file, "-d", "--build"])