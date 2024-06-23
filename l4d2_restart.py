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
def l4d2_map_rand():
    i = random.randint(1, 14)
    if i == 1:
        return "c1m1_hotel"
    elif i == 2:
        return "c2m1_highway"
    elif i == 3:
        return "c3m1_plankcountry"
    elif i == 4:
        return "c4m1_milltown_a"
    elif i == 5:
        return "c5m1_waterfront"
    elif i == 6:
        return "c6m1_riverbank"
    elif i == 7:
        return "c7m1_docks"
    elif i == 8:
        return "c8m1_apartment"
    elif i == 9:
        return "c9m1_alleys"
    elif i == 10:
        return "c10m1_caves"
    elif i == 11:
        return "c11m1_greenhouse"
    elif i == 12:
        return "c12m1_hilltop"
    elif i == 13:
        return "c13m1_alpinecreek"
    elif i == 14:
        return "c14m1_junkyard"
    return "c1m1_hotel"


#
def l4d2_restart_update():
    l4d2_screen_stop('screen -dmS')
    time.sleep(4)
    os.system("./steamcmd/steamcmd.sh +login anonymous +force_install_dir ./l4d2/ +app_update 222860 +validate +quit")
    time.sleep(2)
    os.system(
        "screen -dmS l4d2 ./steamcmd/l4d2/srcds_run -game left4dead2 -port {0} +map {1} -maxplayers {2} -secure +sv_lan 0 -tickrate 66".format(
            sg_port, l4d2_map_rand(), sg_max_players))


#
if os.path.exists('steamcmd'):
    f2.write("\nrestart & start & update [{}]\n".format(time.ctime()))
    l4d2_restart_update()
else:
    f2.write("\n./l4d2_install.sh\n")

#
os.remove('l4d2.dat')
f2.close()
