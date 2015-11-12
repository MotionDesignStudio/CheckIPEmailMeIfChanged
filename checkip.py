#!/usr/bin/env python3.4

#This only works with a Gmail accounts.  You must enable third part applications to have access to your account.

#Follow this URL for information on how to enable this.

#https://www.google.com/settings/security/lesssecureapps

from urllib.request import urlopen
from urllib.error import URLError
import json

#Begin imports for sending emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#End imports for sending emails

#Open file that contains previously saved IP address
savedip = open('/full/path/to/myipis.txt', 'r+')

#Begin function to send email if IP address is different
def sendmeaemail(myip): 
	fromaddr = "my_gmail_email@gmail.com"
	toaddr = "some_recipient@a_email_provide.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Your New IP: "+ myip
	 
	body = "Your New IP: "+ myip
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, 'your_gmail_password')
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

#End function to send email if IP address is different


try:
	url = 'http://api.hostip.info/get_json.php'
	info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))

	if (info['ip']== savedip.readline().strip()):
		print ('yes')
	else:
		#If IP address is different it is time to send a message
		print ('IP address is different')
		savedip.seek(0)
		savedip.truncate()
		savedip.write(info['ip'])
		sendmeaemail(info['ip'])
	savedip.close()

except URLError as e:
	print(e.reason, end=' ') # e.g. 'timed out'
	print('(are you connected to the internet?)')
except KeyboardInterrupt:
	pass

 

