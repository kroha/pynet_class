#!/home/arudas/venv/bin/python

'''
Uptime when running config last changed
ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   

Uptime when running config last saved (note any 'write' constitutes a save)    
ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   

Uptime when startup config last saved   
ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'
'''

import snmp_helper
import pickle
import os
import smtplib

from email.mime.text import MIMEText

rtr1_ip =   '50.76.53.27'
rtr1_user = 'pysnmp'
rtr1_auth = 'galileo1'
rtr1_encr = 'galileo1'
rtr1_snmp = (rtr1_user,rtr1_auth,rtr1_encr)
rtr1 = (rtr1_ip,7961)
rtr2 = (rtr1_ip,8061)

def current_time():
    oid_uptime = '1.3.6.1.4.1.9.9.43.1.1.1.0'
    snmp_raw = snmp_helper.snmp_get_oid_v3(rtr1,rtr1_snmp,oid=oid_uptime)
    snmp_dec = snmp_helper.snmp_extract(snmp_raw)
    return snmp_dec

def time_load():
    time = range(1)
    if os.stat("/home/arudas/git/pynet_class/class3/c3_hw01.pkl").st_size == 0:
       time[0] = 0
       return time
    else:
        f = open("/home/arudas/git/pynet_class/class3/c3_hw01.pkl","rb")
        time = pickle.load(f)
        f.close()
        return time

def time_save(data):
    f = open("/home/arudas/git/pynet_class/class3/c3_hw01.pkl","wb")
    pickle.dump(data,f)
    f.close()
    return 1

def email_send(router, time):
    message = "Change detected: " + str(router) + " at " + str(time)
    sender = 'pynet@rtr1.com'
    recipient = 'andrew.rudas@gmail.com'
    subject = "Change detected: " + str(router)

    message = MIMEText(message)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    smtp_conn = smtplib.SMTP('localhost')
    smtp_conn.sendmail(sender, recipient, message.as_string())

    smtp_conn.quit()

    return True

def main():
    time = current_time()
    old_time = time_load()
    if time > old_time[0]:
        print "..cfg change detected, : " + str(old_time[0]) + " new time: " + str(time)
        old_time.append(time)
        old_time.pop(0)
        time_save(old_time)
        email_send(rtr1,old_time)
    else:
        print "..no changes"

if __name__ == "__main__":
    main()

