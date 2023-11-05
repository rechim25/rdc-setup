#!/bin/sh

# Ensure the username environment variable is set
if [[ -z "${USERNAME}" ]]; then
  echo "The USERNAME environment variable is not set. Exiting."
  exit 1
fi

sudo apt-get install xrdp

sudo systemctl enable xrdp
sudo systemctl start xrdp

sudo ufw allow 3389/tcp

polkit_config_str="[Allow Network Manager for Myself]
Identity=unix-user:$USER
Action=org.freedesktop.NetworkManager.*
ResultAny=yes
ResultInactive=yes
ResultActive=yes

[Allow Login, Shutdown, Restart, Etc for Myself]
Identity=unix-user:USERNAME
Action=org.freedesktop.login1.*
ResultAny=yes
ResultInactive=yes
ResultActive=yes

[Allow Colord all Users]
Identity=unix-user:*
Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
ResultAny=no
ResultInactive=no
ResultActive=yes

[Allow Package Management all Users]
Identity=unix-user:*
Action=org.freedesktop.packagekit.system-sources-refresh
ResultAny=yes
ResultInactive=yes
ResultActive=yes"

polkit_config_file="/etc/polkit-1/localauthority/50-local.d/45-remote-desktop-sanity.pkla"

if [[ -s $polkit_config_file ]]; then
    echo "Polkit config is not empty. Exiting..."
	exit 1
fi
sudo echo "$polkit_config_str" > "$polkit_config_file" && echo "Polkit config updated in $polkit_config_file"