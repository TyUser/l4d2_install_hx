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

# Port l4d2 сервера. По умолчанию 27015
sg_port = 27015

# Максимальное количество игроков l4d2 сервера
sg_max_players = 18


#
def check_l4d2():
    with open("l4d2.log", 'a') as f:
        if os.path.exists('steamcmd'):
            if os.path.isfile('l4d2.dat'):
                f.write("cron canceled ")
                return False
            else:
                return True
        else:
            f.write("\n./l4d2_install.sh\n")

    return False


#
def get_server_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(3)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except (socket.timeout, OSError):
            return '127.0.0.1'


#
def check_and_create_ip():
    filename = 'server_ip'
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return f.read().strip()
        except ():
            pass

    ip = get_server_ip()
    with open(filename, 'w') as f:
        f.write(ip)
    return ip


#
def l4d2_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5)
        try:
            s.connect((ip, port))
            s.sendto(b'\xFF\xFF\xFF\xFFTSource Engine Query\0', (ip, port))
            s.recv(32)
            return True
        except (socket.timeout, ConnectionError):
            return False


#
def l4d2_live(ip, port):
    if l4d2_server(ip, port):
        return True
    else:
        time.sleep(8)
        if l4d2_server(ip, port):
            return True

    time.sleep(8)
    if l4d2_server(ip, port):
        return True

    return False


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
with open("l4d2.log", 'a') as f1:
    if check_l4d2():
        ip = check_and_create_ip()
        if l4d2_live(ip, sg_port):
            f1.write("ok ")
        else:
            f1.write(f"\ncron restart & start & update [{time.ctime()}]\n")
            l4d2_restart_update()
