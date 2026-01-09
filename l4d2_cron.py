#!/usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-only
# github.com/TyUser/l4d2_install_hx
#
# chmod +x l4d2_cron.py
# python3 ./l4d2_cron.py
#

import os
import random
import socket
import time

# ip адрес l4d2 сервера
sg_ip = '127.0.0.1'

# Port l4d2 сервера. По умолчанию 27015
sg_port = 27015

# Максимальное количество игроков l4d2 сервера
sg_max_players = 18

#
ig_err = 0
f1 = open("l4d2.log", 'a')


def l4d2_server(ip, port):
    error1 = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)

    try:
        s.connect((ip, int(port)))
    except:
        error1 = 1

    if error1 == 0:
        try:
            s.sendto(b'\xFF\xFF\xFF\xFFTSource Engine Query\0', (ip, int(port)))
        except:
            error1 = 1

    if error1 == 0:
        try:
            s.recv(32)
        except:
            error1 = 1

    s.close()
    if error1:
        return 0
    return 1


#
def l4d2_live(ip, port):
    if l4d2_server(ip, port):
        return 1
    else:
        time.sleep(8)
        if l4d2_server(ip, port):
            return 1
    return 0


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
    os.system("./steamcmd/steamcmd.sh +force_install_dir ./l4d2/ +login anonymous +app_update 222860 validate +quit")
    time.sleep(2)
    os.system(
        "screen -dmS l4d2 ./steamcmd/l4d2/srcds_run -game left4dead2 -port {0} +map {1} -maxplayers {2} -secure +sv_lan 0 -tickrate 66".format(
            sg_port, l4d2_map_rand(), sg_max_players))


#
if os.path.exists('steamcmd'):
    ig_err = 0
else:
    f1.write("\n./l4d2_install.sh\n")
    ig_err = 1

#
if os.path.isfile('l4d2.dat'):
    f1.write("cron canceled ")
    ig_err = 1

#
if ig_err == 0:
    if l4d2_live(sg_ip, sg_port):
        f1.write("ok ")
    else:
        time.sleep(4)
        if l4d2_live(sg_ip, sg_port):
            f1.write("ok2 ")
        else:
            f1.write("\ncron restart & start & update [{}]\n".format(time.ctime()))
            l4d2_restart_update()

#
f1.close()
