#! /usr/bin/env python3
import shutil
import psutil

def check_usage(disk):
	du = shutil.disk_usage(disk)
	free = du.free / du.total * 100
	print(f"Disk usage for {disk}: {free:.2f}% free")
	return free > 20

def check_cpu():
	usage = psutil.cpu_percent(1)
	print(f"CPU usage: {usage:.2f}%")
	return usage < 75

if not check_usage("/") or not check_cpu():
	print("ERROR! System not OK")
else:
	print("System OK")