# darwinbox_auto_clockin
## Python script to automatically clock in darwinbox. Uses Mac OSX launchctl to run every 10  minutes. Once it clocks in, it will send message to your mobile too. 

<hr>
###### Author: Gowtham Sai
###### Website: https://gowtham-sai.com
###### Aritcle: blog.gowtham-sai.com (Will be updated soon)
###### Date: 7th Aug, 2016.
###### Purpose: I frustated with darwin box. I don't remember to clock in daily. 
###### What this script do?
######		-- This scritps run automatically checks every minute whether you clocked in or not.
######			If not cloked in, it will clock in for you. 
###### So do I need to run the script?
######		-- No/Yes. (You can set cronjob if you want in your mac/linux) / (Task Schedular in Windows Box)
######
###### Sigstamp: 7h3 !n5|d3r
<hr>
#
#
#
# How to configure:
Open [darwin.py](darwin.py) file and Change Your Email id, Phone Number, Password

    37.    email = 'YOUR EMAIL'
    38.    password = 'YOUR PASSWORD HERE'
    39.    mobile = "MOBILE NUMBER HERE"
        
Open [WAY2SMS.py](Way2SMS.py) file, 
    
    23.    username = 'MOBILE NUMBER HERE'
    24.    password = 'Way2SMS PASSWORD HERE'

#### save darwin.py and way2sms.py files. 
#
#
#
#
# Keep this directory somewhere safe where you don't delete or rename this directory in future.
#
#
# How to use:
            
` Now run setup file. `

        $ sudo python setup.py

# All done. Now, you don't need to worry about darwinbox clock in. Forget it. 
##
# Proof:
` Sample Log file from my mac: `

    Mon Aug  8 03:41:49 2016 [INFO] - Opening Darwinbox.
    Mon Aug  8 03:41:50 2016 [INFO] - Submitting Form.
    Mon Aug  8 03:41:59 2016 [INFO] - Login Sucessful.
    Mon Aug  8 03:42:01 2016 [INFO] - User ID 576fc240f0aac.
    Mon Aug  8 03:42:01 2016 [INFO] - User Clocked Out.
    Mon Aug  8 03:42:01 2016 [INFO] - Attempting to CLOCK IN.
    Mon Aug  8 03:44:09 2016 [INFO] - Opening Darwinbox.
    Mon Aug  8 03:44:10 2016 [INFO] - Submitting Form.
    Mon Aug  8 03:44:18 2016 [INFO] - Login Sucessful.
    Mon Aug  8 03:44:20 2016 [INFO] - User ID 576fc240f0aac.
    Mon Aug  8 03:44:20 2016 [INFO] - User Clocked Out.
    Mon Aug  8 03:44:20 2016 [INFO] - Attempting to CLOCK IN.
    Mon Aug  8 03:44:20 2016 [INFO] - CLOCK IN Failed. Reason: Invalid IP<br/>Mon Aug  8    03:54:22 2016 [INFO] - Opening Darwinbox.
    Mon Aug  8 03:54:23 2016 [INFO] - Submitting Form.
    Mon Aug  8 03:54:31 2016 [INFO] - Login Sucessful.
    Mon Aug  8 03:54:33 2016 [INFO] - User ID 576fc240f0aac.
    Mon Aug  8 03:54:33 2016 [INFO] - User Clocked Out.
    Mon Aug  8 03:54:33 2016 [INFO] - Attempting to CLOCK IN.
    Mon Aug  8 03:54:33 2016 [INFO] - CLOCK IN Failed. Reason: Invalid IP<br/>.
    Mon Aug  8 04:04:34 2016 [INFO] - Opening Darwinbox.
    Mon Aug  8 04:04:35 2016 [INFO] - Submitting Form.
    Mon Aug  8 04:04:43 2016 [INFO] - Login Sucessful.
    Mon Aug  8 04:04:44 2016 [INFO] - User ID 576fc240f0aac.
    Mon Aug  8 04:04:44 2016 [INFO] - User Clocked Out.
    Mon Aug  8 04:04:44 2016 [INFO] - Attempting to CLOCK IN.
    Mon Aug  8 04:04:45 2016 [INFO] - CLOCK IN Failed. Reason: Invalid IP<br/>.





# Debugging:
How to check logs:

* You can chceck logs from /var/log/darwinbox.log
* You can check error form  /var/log/darwinbox.error.log
