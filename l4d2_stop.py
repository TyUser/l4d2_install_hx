#!/usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-only
# github.com/TyUser/l4d2_install_hx
#
# chmod +x l4d2_stop.py
# python3 ./l4d2_stop.py
#

import os
import time

#
f1 = open('l4d2.dat', 'w')
f2 = open("l4d2.log", 'a')


#
def l4d2_screen_stop(name):
    cmd = "ps -aef | grep -i '%s' | grep -v 'grep' | awk '{ print $2 }' > /tmp/hx_d"
    os.system(cmd % name)
    with open('/tmp/hx_d') as f:
        for line in f:
            os.system("screen -r {}.l4d2 -X quit".format(line.rstrip("\n")))


#
l4d2_screen_stop('screen -dmS')
f2.write("\nstop [{}]\n".format(time.ctime()))

#
f1.close()
f2.close()
