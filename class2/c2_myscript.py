#!/home/arudas/venv/bin/python

import telnetlib
import time 

# Class router initializing with vector of connection parameters.
class Router:
    def __init__(self,ip_addr,protocol,port,timeout,username,password):
    # Inint vars
        self.ip_addr = ip_addr
        self.protocol = protocol
        self.port = port
        self.timeout = timeout 
        self.username = username
        self.password = password
    def connect(self):
    # Initializing connection
        remote_conn = telnetlib.Telnet(self.ip_addr, self.port, self.timeout)
        remote_conn.read_until("Username", 15)
        remote_conn.read_very_eager()
        remote_conn.write(self.username + '\n')
        remote_conn.read_until("Password", 15)
        remote_conn.write(self.password + '\n')
        remote_conn.write("terminal length 0" + '\n')
        return remote_conn
    def run(self, conn, cmd):
    # Run commands
        conn.write(cmd + '\n')
        time.sleep(2)
        return conn.read_very_eager()

def main():
    # RTR1 example
    rtr1 = Router("50.76.53.27","telnet",23,10,"pyclass","88newclass")
    rtr1_connection = rtr1.connect()
    output = rtr1.run(rtr1_connection,"show ip int brief")
    print output

main()

