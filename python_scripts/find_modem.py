import os
import serial
import commands
import time
import syslog
import urllib,httplib,urllib2


PATH = "/etc/ppp/peers/docomo"
devs = []
ret = []
flag="False"
iden_mod="Manufacturer: +GMI: HUAWEI TECHNOLOGIES CO., LTD"

def internet_on():	
    try:
        response=urllib2.urlopen('http://google.com',timeout=1)
	flag=True
	print flag
	return flag
    except:
		syslog.syslog('ppp error in except')
		os.system('poff docomo')
		syslog.syslog("Error in network")
		#edit_ppp()
		#send sms
		time.sleep(5)
		os.system('pon docomo')
		time.sleep(15)

def edit_ppp(new_port):
	syslog.syslog("editing")
	f=open('%s'%PATH)
	line=f.readlines()
	s=line[7]
	n=s.split()
	f.close()
	fi=open('%s'%PATH)
	files=fi.read()
	text=files.replace('%s'%s,'%s \n'%new_port)
	fil=open('%s'%PATH,'w+')
	fil.write('%s'%text)

def iden_port():
	raw=commands.getoutput("dmesg | grep 'GSM modem (1-port) converter now attached to'")
	mod=raw.splitlines()
	if (len(mod) == 0):
		ven=commands.getoutput('lsusb|grep "Huawei Technologies"')
		ven_id=ven.split()[5][-4:]
		print ven_id
		commands.getoutput('sudo usb_modeswitch -I -W -c /etc/usb_modeswitch.d/12d1\:%s'%ven_id)
		time.sleep(10)
		raw=commands.getoutput("dmesg | grep 'GSM modem (1-port) converter now attached to'")
		mod=raw.splitlines()
		mod_port=mod[-3:]
		for i in range(len(mod_port)):
			devs.append(mod_port[i][-7:])
	else:
		mod_port=mod[-3:]
		for i in range(len(mod_port)):
			devs.append(mod_port[i][-7:])

def main():
	
	def sendCommand(com):
		ser.write(com+"\r\n")
		time.sleep(2)	
		while ser.inWaiting() > 0:
			msg = ser.readline().strip()
			msg = msg.replace("\r","")
			msg = msg.replace("\n","")
			if msg!="":
				ret.append(msg)
	print devs
	iden_port()
	print devs
	time.sleep(15)
	for i in range(len(devs)):
		syslog.syslog('%s'%devs[i])
		ser=serial.Serial('/dev/%s'%devs[i], baudrate=115200, timeout=.1, rtscts=0)
		sendCommand("ATi")
		print ret
		print('%s'%ret[1])
		if iden_mod in ret:
			print(":)")
			newp=devs[i]
			print newp		
			edit_ppp(newp)
			print("editing done")
			os.system('pon docomo')
			time.sleep(15)
			while flag!="False":
				internet_on()
			os.system('sudo /etc/init.d/network start')
			break
		else:
			print "ddd"
			internet_on()
	syslog.syslog("hello")


if __name__ == "__main__":
	main()
