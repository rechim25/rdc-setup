# rdc-setup
Utility and manual for setting up a Remote Desktop Connection from your Windows machine to a remote Ubuntu machine.

The RDP connection is tunneled through SSH. It first opens up an SSH tunnel from your Windows machine's port 13389 to the remote Ubuntu machine (port can is specified in the `rdc_config.yaml`) file. 
Then the RDP connection is initiated.


Requires: Python 3 and PyYAML


1. Install dependencies
``sh
pip install PyYAML
``

2. Modify the `rdc_config.yaml` file
``sh
hosts:
  - name: <display_name>
    hostname: <remote_host_ip>
    user: <your_remote_user>
    ssh_port: <ssh_port_on_remote>
    rdp_remote_port: <rdp_port_on_remote usually 3389>
``

3. Run the utility:
``sh
python rdc_connect.py
``

Alternatively, you can run the shell script in `remote/rds_remote_setup` on your Ubuntu machine. This will set up everything for you:
``sh
chmod +x remote/rds_remote_setup.sh
./remote/rds_remote_setup.sh
``
This will also disable the "Authentication is required to create a color profile" prompt by changing the Polkit settings.
(Disclaimer: I'm not an expert in Remote Desktop Protocol nor in XRDP, so please make sure to settings in the config file `/remote/rds_remote_setup.sh` are what you want).



