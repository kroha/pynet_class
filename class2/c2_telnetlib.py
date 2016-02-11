#!/usr/bin/env python
'''
Write a script that connects to the lab pynet-rtr1, logins, and executes the
'show ip int brief' command.
'''

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6

class Router:
    def __init__(self):
    # Initialize vars
        self.ip_addr = raw_input("IP address: ")
        self.ip_addr = self.ip_addr.strip()
        self.password = getpass.getpass()
        self.username = 'pyclass'

    def send_command(self, remote_conn, cmd):
    # Run commands (cmd) over the connection to router (renote_conn) returns output
        cmd = cmd.rstrip()
        remote_conn.write(cmd + '\n')
        time.sleep(1)
        return remote_conn.read_very_eager()

    def login(self,remote_conn):
    # Authentication username/pass
        output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
        remote_conn.write(self.username + '\n')
        output += remote_conn.read_until("ssword:", TELNET_TIMEOUT)
        remote_conn.write(self.password + '\n')
        remote_conn.read_very_eager()
        time.sleep(1)
        return output

    def disable_paging(self, remote_conn, paging_cmd='terminal length 0'):
    # Predefined cmd (disable paging)
        return self.send_command(remote_conn, paging_cmd)

    def telnet_connect(self):
    # Intial telnet connection using telnetlib (creating telnet connection object)
        try:
            return telnetlib.Telnet(self.ip_addr, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Connection timed-out")

def main():
    # command to run
    cmd =  'show ip int br'
    
    # rtr object / connection / login / commands / output
    rtr = Router()
    remote_conn = rtr.telnet_connect()
    output = rtr.login(remote_conn)
    output = rtr.disable_paging(remote_conn)
    output = rtr.send_command(remote_conn, cmd)

    print "\n#### Output from command: \"" + cmd + "\""
    print output
    print "\n####"

    remote_conn.close()

if __name__ == "__main__":
    main()
