import sys
import time
import os
import mechanize
import cookielib
from getpass import getpass

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
url = 'http://site23.way2sms.com/content/index.html?'
#op = br.open(url)
#br.select_form(nr=0)
stamp = "\n        +=======================================+\n        |..........Way2SMS Msg Tool v 1.........|\n        +---------------------------------------+\n        |#Author: 7H3 !N5|D3R                   |\n        |#Contact: www.fb.com/Gowtham95india    |\n        |#Date: 10/09/2014                      |\n        |#This tool is made for pentesting.     |\n        |#Changing the Description of this tool |\n        |Won't make you the coder ^_^ !!!       |\n        |#Respect Coderz Plz ^_^                |\n        |#I Take No Responsibilities For The    |\n        |  Use Of This Program !                |\n        +=======================================+\n        |.........  Way2SMS Automation .........|\n        +---------------------------------------+\n"
#print stamp
username = 'mobile_number_goes_here'
password = 'password_goes_here'
token = ''


def login():
    global username
    global token
    global password
    op = br.open(url)
    br.select_form(nr=1)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()
    a = br.geturl()
    if username in br.geturl():
        print "[-] Login Failed."
        time.sleep(3)
        print "[-] Exiting Now..."
        time.sleep(3)
        os.system('clear')
        sys.exit()
        return False
    else:
        i = a.index('=')
        j = a.index('?')
        token = a[i + 1:j]
        return token


def send(mobile, message):
    smsurl = 'http://site23.way2sms.com/sendSMS?Token=' + token
    br.open(smsurl)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                     ('Referer', 'http://site25.way2sms.com/sendSMS?Token=' + token)]
    br.select_form(nr=0)
    br.form.set_all_readonly(False)
    message += ' ' * (140 - len(message))
    br.form['mobile'] = mobile
    br.form['message'] = message
    br.form['msgLen'] = str(140)
    br.form.method = 'POST'
    sendurl = 'http://site23.way2sms.com/smstoss.action'
    br.form.action = sendurl
    br.form.fixup()
    res = br.submit()
    if 'status=0' in br.geturl():
        sys.stdout.write(time.ctime()+" [INFO] - Mobile Notification sent sucessfully to %s\n"%mobile)
	return True
    else:
	sys.stdout.write(time.ctime()+" [INFO] - Mobile Notification sent Failed to %s\n"%mobile)
        return False
