#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       network.py
#       
#       Copyright 2011 ganesh <ganesh@space-kerala.org>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


from os import fork, chdir, setsid, umask
from sys import exit
import serial,os
import time,sys
from datetime import datetime
import commands
import syslog,os
import urllib,httplib,urllib2

count = 1
PATH = "/etc/ppp/peers/docomo"
v=""

def timestamp():
	FORMAT = '%Y-%m-%d;%H-%M-%S'
	STAMP = '%s' % (datetime.now().strftime(FORMAT))
	return STAMP

def upload(data):
	params = urllib.urlencode({'rdata' : '%s\n'%data})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("linode.space-kerala.org:80")
	conn.request("POST", "/data.php",params, headers)
	response = conn.getresponse()
	#print response.status, response.reason
	data = response.read()
	#print data
	conn.close()



def edit_ppp():
	newp=dev()
	if (newp == "port error"):
		syslog.syslog("No Valid port identifies")
	else:
		f=open('%s'%PATH)
		line=f.readlines()
		s=line[7]
		n=s.split()
		f.close()
		fi=open('%s'%PATH)
		files=fi.read()
		text=files.replace('%s'%s,'%s \n'%newp)
		fil=open('%s'%PATH,'w+')
		fil.write('%s'%text)

def dev():
	os.system('touch /tmp/dev.txt')
	os.system('wvdialconf > /tmp/dev.txt')
	file=open('/tmp/dev.txt','r+')
	re=file.read()
	f=re.splitlines()
	b=f[5]
	port_dev=b[-8:-1]
	print port_dev
	if port_dev[:6]=="ttyUSB":
		return port_dev
	else:
		syslog.syslog("port error")


def internet_on():	
    try:
        response=urllib2.urlopen('http://google.com',timeout=1)
    except:
		syslog.syslog('ppp error in except')
		os.system('poff docomo')
		syslog.syslog("Error in network")
		#edit_ppp()
		#send sms
		time.sleep(5)
		os.system('pon docomo')
		time.sleep(20)

def main():	
	#time.sleep(50)
	#raw=commands.getoutput("dmesg | grep 'pl2303 converter now attached to'")
	#port=raw[-7:]
	#print port
	#syslog.syslog('prolific port %s'%port)
	#ser = serial.Serial("/dev/%s"%port, 9600, timeout=1)
	#os.system('pon docomo')
	#time.sleep(15)
	while count!=0:
		time.sleep(50)
		raw=commands.getoutput("dmesg | grep 'pl2303 converter now attached to'")
		port=raw[-7:]
		print port
		syslog.syslog('prolific port %s'%port)
		ser = serial.Serial("/dev/%s"%port, 9600, timeout=1)
		os.system('pon docomo')
		time.sleep(20)	
		internet_on()
		syslog.syslog("Internet available")
		time.sleep(5)
		ser.flushInput()
		data=ser.readline()
		#print data
		TIME=timestamp()
		if data!='':
		   file=open('/var/www/serial.txt','a')
		   file.write('%s: '%TIME+data+'\n')
		   v='%s'%TIME+data+'\n'
		   #print len(v)
		   internet_on()
		   syslog.syslog("Internet available")
		   time.sleep(5)
		   if len(v) > 54:
			try:
	   			upload(v)
				syslog.syslog("Uploaded sucessful")
			except:
				syslog.syslog("Couldnt upload")
		   else:
			try:
			   	v="Insufficient Data"
				upload(v)
				syslog.syslog("Uploaded sucessful")
			except:
				syslog.syslog("Couldnt upload")
		ser.close()
		os.system('poff docomo')
		time.sleep(600)

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
