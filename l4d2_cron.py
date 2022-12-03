#!/usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-only
# github.com/TyUser/l4d2_install_hx
#
# chmod +x l4d2_cron.py
# python3 ./l4d2_cron.py
#

import os
import socket
import time

# ip адрес l4d2 сервера
sg_ip = '62.113.112.155'

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
    if l4d2_live(sg_ip, 27015):
        f1.write("ok ")
    else:
        time.sleep(4)
        if l4d2_live(sg_ip, 27015):
            f1.write("ok2 ")
        else:
            f1.write("\ncron restart & start & update [{}]\n".format(time.ctime()))
            l4d2_restart_update()

#
f1.close()
