#! /usr/bin/env python

from os import fork, chdir, setsid, umask
from sys import exit
import serial,os
import time
from datetime import datetime
import commands



def main():

   def timestamp():
	FORMAT = '%Y-%m-%d;%H-%M-%S'
	STAMP = '%s' % (datetime.now().strftime(FORMAT))
	return STAMP
   time.sleep(120)
   raw=commands.getoutput("dmesg | grep 'FTDI USB Serial Device converter now attached to'")
   port=raw[-7:]
   ser = serial.Serial("/dev/%s"%port, 9600, timeout=1)
   while True:
       #ser.flush()
       data=ser.readline()
       #print data
       TIME=timestamp()
       if data!='':
           file=open('/var/www/serial.txt','a')
           file.write('%s: '%TIME+data+'\n')
           #time.sleep(60)
       #ser.flushInput()
       #ser.flushOutput()



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
