Last login: Mon Sep 15 14:35:28 on ttys000
daniel@macbookpro ~ % #!/usr/bin/env python3
import shutil
import psutil

def check_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20

def check_cpu():
    usage = psutil.cpu_percent(1)
    return usage < 75

if not check_usage("/") or not check_cpu():
    print("ERROR!")
else:
    print("Fine")






