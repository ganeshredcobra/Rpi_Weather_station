#! /usr/bin/env python

from os import fork, chdir, setsid, umask
from sys import exit
import serial,os
import time
from datetime import datetime
import commands
import syslog
import urllib,httplib


#def main():

def timestamp():
	FORMAT = '%Y-%m-%d;%H-%M-%S'
	STAMP = '%s' % (datetime.now().strftime(FORMAT))
	return STAMP

def upload():
	params = urllib.urlencode({'rdata' : '%s\n'%v})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("c11.space-kerala.org:80")
	conn.request("POST", "/data.php",params, headers)
	response = conn.getresponse()
	#print response.status, response.reason
	data = response.read()
	#print data
	conn.close()


#time.sleep(60)
#os.system('python wvdial.py')
#time.sleep(60)
raw=commands.getoutput("dmesg | grep 'pl2303 converter now attached to'")
port=raw[-7:]
syslog.syslog('prolific port %s'%port)
ser = serial.Serial("/dev/%s"%port, 9600, timeout=1)
while True:
	#ser.flush()
	ser.flushInput()
	data=ser.readline()
	#print data
	TIME=timestamp()
	if data!='':
	   file=open('/var/www/serial.txt','a')
	   file.write('%s: '%TIME+data+'\n')
	   #try:
	   v='%s'%TIME+data+'\n'
	   upload()
	   time.sleep(60)
	   #ser.flushInput()
	   #ser.flushOutput()
	   #except:
	   #    pass




"""# Dual fork hack to make process run as a daemon
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

main()"""
