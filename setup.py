import os
import sys
import mylog
import re
from getpass import getpass
from ConfigParser import SafeConfigParser

sudo_pass = getpass("Enter sudo Password:")


def setup():
	pwd_path = os.popen('pwd').readlines()[0].strip()
	mylog.log("INFO", "creating launched job for you :)")
	filedir = os.path.dirname(__file__)
	filepath = os.path.join(filedir,'com.darwinbox.Helper.plisttemp')
	program_file = open(filepath,'r')
	actulprogram = []
	for line in program_file.readlines():
		if 'path_to_program' in line: line = line.replace('path_to_program', pwd_path+'/darwin.py')
		actulprogram.append(line)
	program_file.close()
	filepath = os.path.join(filedir,'com.darwinbox.Helper.plist')
	with open(filepath,'w') as program_file:
		for line in actulprogram:
			program_file.write(line)
	mylog.log("INFO", "Configuration for launched job done.")	
	os.popen("echo %s| sudo -S cp -r ./com.darwinbox.Helper.plist /Library/LaunchDaemons/"%sudo_pass)
	mylog.log("INFO", "Loading Launchedjob - com.darwinbox.Helper.plist")	
	os.popen("echo %s | sudo -S launchctl load -w /Library/LaunchDaemons/com.darwinbox.Helper.plist"%sudo_pass)
	mylog.log("INFO", "Starting Launchedjob - com.darwinbox.Helper.plist ")	
	os.popen("echo %s | sudo -S launchctl start /Library/LaunchDaemons/com.darwinbox.Helper.plist"%sudo_pass)
	mylog.log("INFO", "Allset! ")	
	mylog.log("INFO", "chceck /var/log/darwinbox.log for information! ")	


def main():
	parser = SafeConfigParser()
	parser.read('clockin.cfg')
	while not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", str(parser.get('Darwinbox', 'email'))):
		email = raw_input("Please enter a valid email for darwinbox username:\n")
		parser.set('Darwinbox', 'email', email)
		with open('clockin.cfg', 'wb') as configfile:
			parser.write(configfile)
		mylog.log("INFO", "Darwinbox emails set")
	if str(parser.get('Darwinbox', 'password')) == 'password_goes_here':
		password = getpass("Please enter your darwinbox password:\n")
		parser.set('Darwinbox', 'password', password)
		mylog.log("INFO", "Darwinbox password set")
	if str(parser.get('Darwinbox', 'sms_notif_enabled')) == 'True_or_False':
		sms_notif_enable = raw_input("Would you like to receive SMS notifications?[yN]:")
		sms_notif_enable = 'True' if (sms_notif_enable.lower == "yes" or sms_notif_enable.lower == "y") else 'False'
		parser.set('Darwinbox', 'sms_notif_enabled', sms_notif_enable)
		with open('clockin.cfg', 'wb') as configfile:
			parser.write(configfile)
	if parser.getboolean('Darwinbox', 'sms_notif_enabled'):
		if str(parser.get('Darwinbox', 'mobile')) == 'mobile_number_goes_here':
			mobile = raw_input("Enter mobile number to send sms notifications")
			parser.set('Darwinbox', 'mobile', mobile)
			mylog.log("INFO", "set mobile number to send sms notifications")
		if str(parser.get('Way2SMS', 'username')) == 'mobile_number_goes_here':
			mobile = raw_input("Enter mobile number to login to Way2SMS")
			parser.set('Way2SMS', 'username', mobile)
			mylog.log("INFO", "set username to Way2SMS login")
		if str(parser.get('Way2SMS', 'password')) == 'password_goes_here':
			password = getpass("Please enter your Way2SMS password")
			parser.set('Way2SMS', 'password', password)
			mylog.log("INFO", "Way2SMS password set")
	with open('clockin.cfg', 'wb') as configfile:
		parser.write(configfile)
	try:
		import mechanize
		setup()
	except ImportError:
		mylog.log("ERROR","Can't import mechanize. No Moudle Found in Local! :(")
		mylog.log("INFO", "I got that covered it for you ;)")
		mylog.log("INFO", "Installing mechanize Moudle from Online. :-p")	
		importlog = os.popen("echo %s | sudo -S easy_install mechanize"%sudo_pass)
		if 'finished' in importlog.readlines()[-1].lower():
			mylog.log("INFO", "Successfully Installed mechanize moudle")
			setup()
		else:
			mylog.log("FATAL", "Installing mechanize moudle Failed. :(")
			mylog.log("INFO", "Existing Setup.")
			sys.exit("Unknow Error..!")

if __name__ == '__main__':
	main()
