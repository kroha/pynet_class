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
import pygal
import pprint
from email.mime.text import MIMEText

rtr1_ip =   '50.76.53.27'
rtr1_user = 'pysnmp'
rtr1_auth = 'galileo1'
rtr1_encr = 'galileo1'
rtr1_snmp = (rtr1_user,rtr1_auth,rtr1_encr)
rtr1 = (rtr1_ip,7961)
rtr2 = (rtr1_ip,8061)
fa4_in_octets = []
fa4_out_octets = []
fa4_in_packets = []
fa4_out_packets = []
fa4_description = '' 
all_data = []

EMPTY = False

oids = [('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5'),
    ('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5'),
    ('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5'),
    ('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
    ('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')]

def update_data(NEW,description,in_octets,in_packets,out_octets,out_packets):
    for name,oid in oids:
        if name == 'ifDescr_fa4':
            snmp_raw = snmp_helper.snmp_get_oid_v3(rtr1,rtr1_snmp,oid=oid)
            snmp_dec = snmp_helper.snmp_extract(snmp_raw)
            description = snmp_dec
        if name == 'ifInOctets_fa4':
            snmp_raw = snmp_helper.snmp_get_oid_v3(rtr1,rtr1_snmp,oid=oid)
            snmp_dec = snmp_helper.snmp_extract(snmp_raw)
            if NEW == True:
                in_octets.insert(0,int(snmp_dec))
            else:
                in_octets.insert(1,int(snmp_dec) - in_octets[0])
                in_octets[0] = int(snmp_dec)
                in_octets = in_octets[:13]
        if name == 'ifInUcastPkts_fa4':
            snmp_raw = snmp_helper.snmp_get_oid_v3(rtr1,rtr1_snmp,oid=oid)
            snmp_dec = snmp_helper.snmp_extract(snmp_raw)
            if NEW == True:
                in_packets.insert(0,int(snmp_dec))
            else:
                in_packets.insert(1,int(snmp_dec) - in_packets[0])
                in_packets[0] = int(snmp_dec)
                in_packets = in_packets[:13]
        if name == 'ifOutOctets_fa4':
            snmp_raw = snmp_helper.snmp_get_oid_v3(rtr1,rtr1_snmp,oid=oid)
            snmp_dec = snmp_helper.snmp_extract(snmp_raw)
            if NEW == True:
                out_octets.insert(0,int(snmp_dec))
            else:
                out_octets.insert(1,int(snmp_dec) - out_octets[0])
                out_octets[0] = int(snmp_dec)
                out_octets = out_octets[:13]
        if name == 'ifOutUcastPkts_fa4':
            snmp_raw = snmp_helper.snmp_get_oid_v3(rtr1,rtr1_snmp,oid=oid)
            snmp_dec = snmp_helper.snmp_extract(snmp_raw)
            if NEW == True:
                out_packets.insert(0,int(snmp_dec))
            else:
                out_packets.insert(1,int(snmp_dec) - out_packets[0])
                out_packets[0] = int(snmp_dec)
                out_packets = out_packets[:13]
    return(description,in_octets,in_packets,out_octets,out_packets)

def data_load(NEW):
    if NEW == True:
        f = open("/home/arudas/git/pynet_class/class3/c3_hw02.pkl","wb")
        description = "Interface FA4"
        in_octets = range(1)
        in_packets = range(1)
        out_octets = range(1)
        out_packets = range(1)
        data = [description,in_octets,in_packets,out_octets,out_packets]
        pickle.dump(data,f)
        f.close()
        return(data)
    else:
        f = open("/home/arudas/git/pynet_class/class3/c3_hw02.pkl","rb")
        data = pickle.load(f)
        f.close()
        # print "load data fun from existing: " + str(data)
        EMPTY = False
        return data

def data_save(data):
    f = open("/home/arudas/git/pynet_class/class3/c3_hw02.pkl","wb")
    pickle.dump(data,f)
    f.close()
    return 1

'''
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
'''
def draw_data(data):
    line_chart_octet = pygal.Line() 
    line_chart_packet = pygal.Line()

    line_chart_octet.title = 'Last hour Input/Output octets for ' + str(data[0])
    line_chart_packet.title = 'Last hour Input/Output packets for ' + str(data[0])

    line_chart_octet.x_labeles = ['0','5','10','15','20','25','30','35','40','45','50','55']
    line_chart_packet.x_labeles = ['0','5','10','15','20','25','30','35','40','45','50','55']
    
    line_chart_octet.add = ('In Bytes', data[1][1:])
    line_chart_octet.add = ('Out Bytes', data[3][1:])
   
    line_chart_packet.add = ('In Packets', data[2][1:])
    line_chart_packet.add = ('Out Packets', data[4][1:])
   
    line_chart_octet.render_to_file('/home/arudas/git/pynet_class/class3/in_out_octets.svg')
    line_chart_packet.render_to_file('/home/arudas/git/pynet_class/class3/in_out_packets.svg')

    line_chart_octet.render_to_png('/home/arudas/git/pynet_class/class3/in_out_octets.png')
    line_chart_packet.render_to_png('/home/arudas/git/pynet_class/class3/in_out_packets.png')
def main():
    if os.stat("/home/arudas/git/pynet_class/class3/c3_hw02.pkl").st_size == 0:
        EMPTY = True
    else:
        EMPTY = False

    all_data = data_load(EMPTY)
    
    fa4_description = all_data[0]
    fa4_in_octets = all_data[1]
    fa4_in_packets = all_data[2]
    fa4_out_octets = all_data[3]
    fa4_out_packets = all_data[4]
    
    all_data = update_data(EMPTY,fa4_description,fa4_in_octets,fa4_in_packets,fa4_out_octets,fa4_out_packets)
    
    data_save(all_data)
    draw_data(all_data)    

    pprint.pprint(all_data)

    # email_send(rtr1,old_time)

if __name__ == "__main__":
    main()

