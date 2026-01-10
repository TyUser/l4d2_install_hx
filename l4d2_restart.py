#!/usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-only
# github.com/TyUser/l4d2_install_hx
#
# chmod +x l4d2_restart.py
# python3 ./l4d2_restart.py
#

import os
import random
import time

# port l4d2 сервера
sg_port = 27015

# Максимальное количество игроков l4d2 сервера
sg_max_players = 18

#
f1 = open('l4d2.dat', 'w')
f1.close()


#
def l4d2_screen_stop(name):
    cmd = "ps -aef | grep -i '%s' | grep -v 'grep' | awk '{ print $2 }' > /tmp/hx_d"
    os.system(cmd % name)
    with open('/tmp/hx_d') as f:
        for line in f:
            os.system("screen -r {}.l4d2 -X quit".format(line.rstrip("\n")))


#
def l4d2_map_rand():
    maps = ["c1m1_hotel", "c2m1_highway", "c3m1_plankcountry", "c4m1_milltown_a", "c5m1_waterfront", "c6m1_riverbank",
            "c7m1_docks", "c8m1_apartment", "c9m1_alleys", "c10m1_caves", "c11m1_greenhouse", "c12m1_hilltop",
            "c13m1_alpinecreek", "c14m1_junkyard"]
    return random.choice(maps)


#
def l4d2_restart_update():
    l4d2_screen_stop('screen -dmS')
    time.sleep(4)
    os.system("./steamcmd/steamcmd.sh +force_install_dir ./l4d2/ +login anonymous +app_update 222860 validate +quit")
    time.sleep(2)
    os.system(
        "screen -dmS l4d2 ./steamcmd/l4d2/srcds_run -game left4dead2 -port {0} +map {1} -maxplayers {2} -secure +sv_lan 0 -tickrate 66".format(
            sg_port, l4d2_map_rand(), sg_max_players))


#
with open("l4d2.log", 'a') as f2:
    if os.path.exists('steamcmd'):
        f2.write(f"\nrestart & start & update [{time.ctime()}]\n")
        l4d2_restart_update()
    else:
        f2.write("\n./l4d2_install.sh\n")


#
os.remove('l4d2.dat')
