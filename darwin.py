#!/usr/bin/env python2.7
#
# Author: Gowtham Sai
# Website: https://gowtham-sai.com
# Aritcle: blog.gowtham-sai.com (Will be updated soon)
# Date: 7th Aug, 2016.
# Purpose: I frustated with darwin box. I don't remember to clock in daily. 
# What this script do?
#		-- This scritps run automatically checks every minute whether you clocked in or not.
#				If not cloked in, it will clock in for you. 
# So do I need to run the script?
#		-- No/Yes. (You can set cronjob if you want in your mac/linux) / (Task Schedular in Windows Box)
#
# Sigstamp: 7h3 !n5|d3r
		
import mechanize
import cookielib
import Way2SMS
import json
import os
import time
import sys

# Browser Setup
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


# Logger Initialization
filedir = os.path.dirname(__file__)
filepath = os.path.join(filedir,'log.txt')
logger = open(filepath,'a')

def ok(msg,purpose):
        logger.write(time.ctime()+': %s - %s.\n'%(purpose,msg))
        print time.ctime()+": %s - %s."%(purpose,msg)


# Darwinbox credentials
email = 'YOUR EMAIL HERE'
password = 'YOUR PASSWORD HERE'
mobile = "MOBILE NUMBER HERE"
value = email.replace('@', '.')

loginurl = 'https://voonik.darwinbox.in/user/login'
clockurl = 'https://voonik.darwinbox.in/attendance/attendance/log?user='

sys.stdout.write(time.ctime()+" [INFO] - Opening Darwinbox.\n")
try:
	login = br.open(loginurl)
except Exception as e:
	sys.stdout.write(time.ctime()+" [FATAL] - Opening Darwinbox Failed. %s\n"%e.message)
	sys.stderr.write(time.ctime()+" [FATAL] - Opening Darwinbox Failed. %s\n"%e.message)

login.set_data(login.get_data().replace('<form  role="form">', ''))
br.set_response(login)
br.select_form(nr=0)
br.form['UserLogin[username]'] = email
br.form['UserLogin[password]'] = password

sys.stdout.write(time.ctime()+" [INFO] - Submitting Form.\n")

try:
	br.submit()
	if br.geturl() != loginurl:
		sys.stdout.write(time.ctime()+" [INFO] - Login Sucessful.\n")
		page = br.response().read()
		firstmatch = page.find(value)
		startpos = page[firstmatch::-1].find('{')
		userdata = json.loads(page[firstmatch-startpos:firstmatch+page[firstmatch:].find('}')+1].replace("'", '"'))
		sys.stdout.write(time.ctime()+" [INFO] - User ID %s.\n"%userdata['id'])
		for link in br.links():
			if 'clock in' in link.text.lower():
				sys.stdout.write(time.ctime()+" [INFO] - User Clocked Out.\n")
				clockurl = clockurl+str(userdata['id'])
				xhr = mechanize.Request(clockurl)
				xhr.add_header('X-Requested-With', 'XMLHttpRequest')
				xhr.add_header('Accept', 'application/json, text/javascript, */*')
				sys.stdout.write(time.ctime()+" [INFO] - Attempting to CLOCK IN.\n")
				try:
					data = json.loads(br.open_novisit(xhr).readlines()[-1])
					if not data.has_key('error'):
						sys.stdout.write(time.ctime()+" [INFO] - User Sucessfully Clocked In.\n")
						ok("Sucessfully Clocked In. ","Info")
						log = Way2SMS.login()
						if log != False:	
							sys.stdout.write(time.ctime()+" [INFO] - Sending Notification to mobile - %s\n"%mobile)		
							try:
								Way2SMS.send(mobile, time.ctime()+": %s - %s."%("Info","Sucessfully Clocked In. %s" % resp.code,))
							except Exception as e:
								sys.stdout.write(time.ctime()+" [FATAL] - Moblie Notification Failed. %s\n"%e.message)
								sys.stderr.write(time.ctime()+" [FATAL] - Moblie Notification Failed. %s\n"%e.message)
							break
					else:
						sys.stdout.write(time.ctime()+" [INFO] - CLOCK IN Failed. Reason: %s.\n"%data['error'])
				except Exception as e:
					sys.stdout.write(time.ctime()+" [FATAL] - CLOCK IN Failed. %s\n"%e.message)
					sys.stderr.write(time.ctime()+" [FATAL] - CLOCK IN Failed. %s\n"%e.message)

except Exception as e:
	sys.stdout.write(time.ctime()+" [FATAL] - Submitting Form Failed. %s\n"%e.message)
	sys.stderr.write(time.ctime()+" [FATAL] - Submitting Form Failed. %s\n"%e.message)


	
