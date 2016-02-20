#!/home/arudas/venv/bin/python

import Queue
import threading

import datetime
import paramiko
import netmiko
import pexpect
import pprint
import time

ip = '50.76.53.27'
user = 'pyclass'
port = 8022
password = '88newclass'


dev1 = {
    'device_type'   : 'cisco_ios',
    'ip'            : '50.76.53.27',
    'username'      : 'pyclass',
    'password'      : '88newclass',
    'port'          : '22',
}

dev2 = {  
    'device_type'   : 'cisco_ios',
    'ip'            : '50.76.53.27',
    'username'      : 'pyclass',
    'password'      : '88newclass',
    'port'          : '8022',
}
dev3 = {
    'device_type'   : 'juniper',
    'ip'            : '50.76.53.27',
    'username'      : 'pyclass',
    'password'      : '88newclass',
    'port'          : '9822',

}

devs = [dev1, dev2, dev3] 

def init_lab1_2():
    conn = paramiko.SSHClient()
    conn.load_system_host_keys()
    conn.connect(ip,username=user,password=password,look_for_keys=False,allow_agent=False,port=port)
    return conn

def init_lab3_4():
    conn = pexpect.spawn('ssh -l {} {} -p {}'.format (user, ip, port))
    conn.timeout = 10
    conn.expect('ssword:')
    conn.sendline(password)
    conn.expect('#')
    return conn

def init_lab5_8(device):
    datetime
    conn = netmiko.ConnectHandler(**device)
    return conn

def send_data(r_conn,cmd,time_sleep):
    r_conn.send(cmd)
    time.sleep(time_sleep)
    output = r_conn.recv(65535)
    return output

def lab1(r_conn):
    # show run via paramiko
    output = send_data(r_conn,"terminal length 0\n",0.1)
    output = send_data(r_conn,"show run\n",2)

    print "\nlab 1: show run: \n\n" + str(output)

def lab2(r_conn):
    # chages via paramiko
    output = send_data(r_conn,"conf t\n",0.2)
    output = send_data(r_conn,"logging buffered 60000\n",0.2)
    output = send_data(r_conn,"end\n",0.2)
    output = send_data(r_conn,"sh run | i logging\n",2)
    print "\nlab 2: buffer changes: \n\n" + str(output)

def lab3_4(conn):
    # change / show run via pexpect
    conn.sendline("show ip int brief")
    conn.expect('#')
    print "\nLab3: print show ip int br:\n" + str(conn.before)

    conn.sendline("configure terminal")
    conn.expect('#')
    conn.sendline("logging buffered 600010")
    conn.expect('#')
    conn.sendline("end")
    conn.expect('#')
    conn.sendline("terminal length 0")
    conn.expect('#')
    
    try:
        conn.sendline('show run')
        conn.expect("pynet-rtr2#")
    except pexpect.TIMEOUT:
        print "Found timeout"

    print "\nLab4: change buffer size and print show run:\n" + str(conn.before)
    
def lab5_8(qu,dev):

    # Lab 9 - multithreading timers
    print "\nStart time for thread/device " + str(dev) + " " + str(datetime.datetime.now()) 

    # multithread with put/get 
    # qu.put(init_lab5_8(dev))
    # conn = qu.get()

    conn = init_lab5_8(dev)
    
    if conn.device_type  == 'cisco_ios':
        if conn.check_config_mode() != True:
            conn.config_mode()
            print "\nLab5:\n I'm in config mode at device: " + str(conn.base_prompt) 
            conn.exit_config_mode()
            output = conn.send_command("sh ip arp")
            print "\nLab6:\nARP Table from device: " + str(conn.base_prompt) + "\n Result: " + str(output)
    elif conn.device_type == 'juniper':
        output = conn.send_command("sh arp")
        print "\nLab6:\nARP Table from device: " + str(conn.base_prompt) + "\n Result:" + str(output)
    if str(conn.base_prompt) == 'pynet-rtr2':
        conn.config_mode()
        output = conn.send_command("logging buffered 680200")
        conn.exit_config_mode()
        output = conn.send_command("show run | i buffered")
        print "\nLab 7:\n log buf changed via netmiko for device: " + str(conn.base_prompt) + "\n Result: \n\t" + str(output) 
    if str(conn.base_prompt) == 'pynet-rtr2' or str(conn.base_prompt) == 'pynet-rtr1':
        conn.send_config_from_file(config_file='cfg_change.txt')
        conn.exit_config_mode()
        output = conn.send_command("show run | i buffered")
        print "\nLab 8:\n log buf changed via file for device: " + str(conn.base_prompt) + "\n Result: \n\t" + str(output)

    print "\nStop time for thread/device " + str(conn.base_prompt) + " " + str(datetime.datetime.now())

def main():
    
    # Lab 1-2

    conn = init_lab1_2()
    r_conn = conn.invoke_shell()

    lab1(r_conn)
    lab2(r_conn)

    # Lab 3-4
    conn = init_lab3_4()
    lab3_4(conn)
    
    # Lab 5-8 + 9
    qu = Queue.Queue()
    for dev in devs:
        thread = threading.Thread(target=lab5_8, args = (qu, dev))
        thread.start()

if __name__ == "__main__":
    main()

