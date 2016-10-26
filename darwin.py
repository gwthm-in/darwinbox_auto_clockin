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
import mylog
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

# Darwinbox credentials
email = 'email_goes_here'
password = 'password_goes_here'
mobile = ""
value = email.replace('@', '.')

loginurl = 'https://voonik.darwinbox.in/user/login'
clockurl = 'https://voonik.darwinbox.in/attendance/attendance/log?user='

mylog.log("INFO", "Opening Darwinbox.")
try:
	login = br.open(loginurl)

	login.set_data(login.get_data().replace('<form  role="form">', ''))
	br.set_response(login)
	br.select_form(nr=0)
	br.form['UserLogin[username]'] = email
	br.form['UserLogin[password]'] = password
	mylog.log("INFO", "Submitting Form.")

	
	br.submit()
	if br.geturl() != loginurl:
		mylog.log("INFO", "Login Sucessful.")
		page = br.response().read()
		firstmatch = page[page.find('data: {user:'):page.find('data: {user:')+30]
		user_id = firstmatch[firstmatch.find('"')+1:firstmatch.find('}')-1]
		mylog.log("INFO", "User ID %s."%user_id)
		has_clock_link = False
		for link in br.links():
			if 'clock in' in link.text.lower():
				has_clock_link = True
				mylog.log("INFO", "User Clocked Out.")
				clockurl = clockurl+user_id
				xhr = mechanize.Request(clockurl)
				xhr.add_header('X-Requested-With', 'XMLHttpRequest')
				xhr.add_header('Accept', 'application/json, text/javascript, */*')
				mylog.log("INFO", "Attempting to CLOCK IN.")
				
				data = json.loads(br.open_novisit(xhr).readlines()[-1])
				if not data.has_key('error'):
					mylog.log("INFO", "User Sucessfully Clocked In.")
					log = Way2SMS.login()
					if log != False:	
						mylog.log("INFO", "Sending Notification to mobile - %s"%mobile)		
						Way2SMS.send(mobile, time.ctime()+": %s - %s."%("Info","Sucessfully Clocked In."))
						break
				else:
					mylog.log("INFO", "CLOCK IN Failed. Reason: %s."%data['error'])
				
		if not has_clock_link:
			mylog.log("INFO", "User Clocked In Already.")

except Exception as e:
	mylog.log("FATAL", "%s"%e.message, sys.exc_info()[-1].tb_lineno)
