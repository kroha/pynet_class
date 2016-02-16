#!/home/arudas/venv/bin/python

import snmp_helper
import pickle
import os
import smtplib
import pygal
import pprint

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

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
time = 0

EMPTY = False

oids = [('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5'),
    ('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5'),
    ('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5'),
    ('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
    ('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')]

def update_data(NEW,description,in_octets,in_packets,out_octets,out_packets,time):
    if time >= 60:
        time = 5
    else:
        time = time + 5
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
    return(description,in_octets,in_packets,out_octets,out_packets,time)

def data_load(NEW):
    if NEW == True:
        f = open("/home/arudas/git/pynet_class/class3/c3_hw02.pkl","wb")
        description = "Interface FA4"
        in_octets = range(1)
        in_packets = range(1)
        out_octets = range(1)
        out_packets = range(1)
        data = [description,in_octets,in_packets,out_octets,out_packets,time]
        pickle.dump(data,f)
        f.close()
        return(data)
    else:
        f = open("/home/arudas/git/pynet_class/class3/c3_hw02.pkl","rb")
        data = pickle.load(f)
        f.close()
        EMPTY = False
        return data

def data_save(data):
    f = open("/home/arudas/git/pynet_class/class3/c3_hw02.pkl","wb")
    pickle.dump(data,f)
    f.close()
    return 1

def email_send(time):
    if time >= 60:
        message = "Graph Interface Fa0/4" 
        sender = 'pynet@rtr1.com'
        recipient = 'andrew.rudas@gmail.com'
        subject = "Interface fa0/4 graphs"

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
    
        msg.preamble = 'Multipart massage.\n'

        part = MIMEText("Graph Interface Fa0/4")
        msg.attach(part)

        part = MIMEApplication(open("/home/arudas/git/pynet_class/class3/in_out_octets.svg","rb").read())
        part.add_header('Content-Disposition', 'attachment', filename="in_out_octets.svg")
        msg.attach(part)

        part = MIMEApplication(open("/home/arudas/git/pynet_class/class3/in_out_packets.svg","rb").read())
        part.add_header('Content-Disposition', 'attachment', filename="in_out_packets.svg")
        msg.attach(part)

        smtp_conn = smtplib.SMTP('localhost')
        smtp_conn.sendmail(sender, recipient, msg.as_string())
        smtp_conn.quit()
    return True

def draw_data(data):
    line_chart_octet = pygal.Line() 
    line_chart_packet = pygal.Line()

    line_chart_octet.title = 'Last hour Input/Output octets for ' + str(data[0])
    line_chart_packet.title = 'Last hour Input/Output packets for ' + str(data[0])

    line_chart_octet.x_labels = ['5','10','15','20','25','30','35','40','45','50','55','60']
    line_chart_packet.x_labels = ['5','10','15','20','25','30','35','40','45','50','55','60']
    
    line_chart_octet.add('In Bytes',data[1][1:])
    line_chart_octet.add('Out Bytes',data[3][1:])
   
    line_chart_packet.add('In Packets',data[2][1:])
    line_chart_packet.add('Out Packets',data[4][1:])
   
    line_chart_octet.render_to_file('/home/arudas/git/pynet_class/class3/in_out_octets.svg')
    line_chart_packet.render_to_file('/home/arudas/git/pynet_class/class3/in_out_packets.svg')

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
    time = all_data[5]

    all_data = update_data(EMPTY,fa4_description,fa4_in_octets,fa4_in_packets,fa4_out_octets,fa4_out_packets,time)

    data_save(all_data)
    draw_data(all_data)    
    
    email_send(all_data[5])

if __name__ == "__main__":
    main()

