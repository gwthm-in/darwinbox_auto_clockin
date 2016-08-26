import os
import sys
import mylog

sudo_pass = raw_input("Enter sudo Password:")


def setup():
	pwd_path = os.popen('pwd').readlines()[0].strip()
	mylog.log("INFO", "creating launched job for you :)")
	filedir = os.path.dirname(__file__)
	filepath = os.path.join(filedir,'com.darwinbox.Helper.plist')
	program_file = open(filepath,'r')
	actulprogram = []
	for line in program_file.readlines():
		if 'path_to_program' in line: line = line.replace('path_to_program', pwd_path+'/darwin.py')
		actulprogram.append(line)
	program_file.close()
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
	filedir = os.path.dirname(__file__)
	msgpath = os.path.join(filedir,'Way2SMS.py')
	darwinpath = os.path.join(filedir,'darwin.py')
	msgfiles = open(msgpath,'r').readlines()
	darwinfiles = open(darwinpath,'r').readlines()
	for msgfile in msgfiles:
		if 'mobile_number_goes_here' in msgfile or 'password_goes_here' in msgfile: 
			mylog.log("FATAL", "Please modify way2sms.py and insert your mobile number and password before continuing.")	
			sys.exit("\n\nInappropriate username or password in way2sms.py file\n")
	for darwinfile in darwinfiles:
		if 'email_goes_here' in darwinfile or 'password_goes_here' in darwinfile or 'mobile_goes_here' in darwinfile:
			mylog.log("FATAL", "Please modify darwin.py and insert your email, darwin box password and mobile before continuing.")	
			sys.exit("\n\nInappropriate username/password/mobile number in darwin.py file\n")
	else:
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
