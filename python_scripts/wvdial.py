#! /usr/bin/env python

from os import fork, chdir, setsid, umask
from sys import exit
import serial,os
import time
from datetime import datetime
import commands,syslog



def main():
	time.sleep(100)
	os.system('sudo usb_modeswitch -c /etc/usb_modeswitch.d/12d1\:1505')
	time.sleep(25)
	os.system('sudo wvdial')
	syslog.syslog('wvdial Processing started')




# Dual fork hack to make process run as a daemon
if __name__ == "__main__":
      try:
        pid = fork()
        if pid > 0:
          exit(0)
      except OSError, e:
        exit(1)

      chdir("/")
      setsid()
      umask(0)

      try:
        pid = fork()
        if pid > 0:
          exit(0)
      except OSError, e:
        exit(1)

main()


