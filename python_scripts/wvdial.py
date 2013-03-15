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
	raw=commands.getoutput("dmesg | grep 'GSM modem (1-port) converter now attached to'")
	port=raw.splitlines()[0][-7:]
	path='/etc/wvdial.conf'
	file=open('%s'%path,'r+')
	new=file.read()
	text=new.replace('Modem = /dev/ttyUSB0','Modem = /dev/%s'%port)
	file=open('%s'%path,'w+')
	file.write('%s'%text)
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


