import yaml
import subprocess
import signal
import socket
import time
import os

tunnel_process = None  # Global variable to hold the SSH process
rdp_process = None


def terminate_processes(signal, frame):
    global tunnel_process, rdp_process
    print("\nExiting")
    if tunnel_process is not None and tunnel_process.poll() is None: # Check if process still running
        tunnel_process.terminate()
    if rdp_process is not None:
        rdp_process.terminate()
    exit(0)
    
    
def is_tunnel_up():
    try:
        with socket.create_connection(("localhost", 13389), timeout=1):
            return True
    except socket.error:
        return False


def main():
    global tunnel_process, rdp_process

    # Set up signal handler for SIGINT (CTRL-C)
    signal.signal(signal.SIGINT, terminate_processes)

    # Load configuration from YAML file
    with open('rdc_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Display menu
    for i, host in enumerate(config['hosts'], start=1):
        print(f"{i}. {host['name']}")
    
    # Prompt user to select remote host
    selection_input = input('Enter number: ')
    try:
        selection = int(selection_input) - 1
    except Exception as e:
        exit(f"Error: {e}")
        
    selected_host = config['hosts'][selection]

    # Create SSH tunnel
    tunnel_cmd = (
        f"ssh -L 13389:localhost:{selected_host['rdp_remote_port']} "
        f"-p {selected_host['ssh_port']} "
        f"{selected_host['user']}@{selected_host['hostname']} -N"
    )
    print("Starting SSH tunnel...")
    print(tunnel_cmd)

    tunnel_process = subprocess.Popen(tunnel_cmd)
    while tunnel_process is not None and not is_tunnel_up():
        if tunnel_process.poll() is not None:
            exit(1)
        time.sleep(1)
    print("SSH tunnel is up!\n")

    try:
        # Start Remote Desktop Connection
        # rdp_command = ['mstsc', '/v:localhost:13389', f"/user:{selected_host['user']}", f'/pass:{rdp_password}']
        rdp_command = ['mstsc', f'{os.getcwd()}\\rdc_client_config.rdc', '/v:localhost:13389', "/f"]
        print("Starting RDP connection...\n")
        rdp_process = subprocess.run(rdp_command, shell=False)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Terminate SSH tunnel
        if tunnel_process is not None and tunnel_process.poll() is None: # Check if process still running
            tunnel_process.terminate()
            print("Terminated SSH tunnel")
        print("Exiting")
        exit(0)

if __name__ == "__main__":
    main()
