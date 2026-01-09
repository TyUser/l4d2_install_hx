#!/bin/bash

# SPDX-License-Identifier: GPL-3.0-only
# github.com/TyUser/l4d2_install_hx
#
# chmod +x ./l4d2_install.sh
# ./l4d2_install.sh
#

echo "-------------START-------------"
#
cd
wget https://www.russerver.com/blog/file/l4d2_server.tar.gz
tar -xvzf l4d2_server.tar.gz
chmod +x l4d2_cron.py
chmod +x l4d2_restart.py
chmod +x l4d2_stop.py
#
#
mkdir ~/steamcmd
cd ~/steamcmd
wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
tar -xvzf steamcmd_linux.tar.gz
./steamcmd.sh +force_install_dir ./l4d2/ +login anonymous +app_update 222860 validate +quit
#
#
cd
mkdir ~/.steam/sdk32/
ln -s steamcmd/linux32/steamclient.so ~/.steam/sdk32/steamclient.so
echo "-------------END-------------"
#
#
cd
rm l4d2_server.tar.gz
rm l4d2_install.sh
