#!/usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-only
# github.com/TyUser/l4d2_install_hx
#
# chmod +x l4d2_restart.py
# python3 ./l4d2_restart.py
#

import os
import time

#
f1 = open('l4d2.dat', 'w')
f2 = open("l4d2.log", 'a')
f1.close()


#
def l4d2_screen_stop(name):
    cmd = "ps -aef | grep -i '%s' | grep -v 'grep' | awk '{ print $2 }' > /tmp/hx_d"
    os.system(cmd % name)
    with open('/tmp/hx_d') as f:
        for line in f:
            os.system("screen -r {}.l4d2 -X quit".format(line.rstrip("\n")))


#
def l4d2_restart_update():
    l4d2_screen_stop('screen -dmS')
    time.sleep(4)
    os.system(
        "./steamcmd/steamcmd.sh +login anonymous +force_install_dir ./l4d2/ +app_update 222860 +validate +quit")
    time.sleep(2)
    os.system(
        "screen -dmS l4d2 ./steamcmd/l4d2/srcds_run -game left4dead2 -port 27015 +map c1m1_hotel -maxplayers 20 -secure +sv_lan 0 -tickrate 66")


#
if os.path.exists('steamcmd'):
    f2.write("\nrestart & start & update [{}]\n".format(time.ctime()))
    l4d2_restart_update()
else:
    f2.write("\n./l4d2_install.sh\n")

#
os.remove('l4d2.dat')
f2.close()
