#!/home/arudas/venv/bin/python

import pyeapi
import pprint
import sys

def main():
    conn = pyeapi.connect_to('pynet-sw3')
    index = 0

    for i in sys.argv:
        index = index + 1
        if i == '--name':
            vlan_name = sys.argv[index]
            vlan_id = sys.argv[index+1]
            print " - adding vlan: " + str(vlan_name) + " ID: " + str(vlan_id)
            run(conn,'add',vlan_id,vlan_name)
            next
        elif i == '--remove':
            vlan_id = sys.argv[index]
            print " - removing vlan: " + str(vlan_id)
            run(conn,'del',vlan_id)
            next 

def run(conn,action,vlan_id=0, name='none'):
    if action == 'add':
        cmd = ['configure terminal','vlan ' + str(vlan_id),'name ' + str(name),'write memory']
        out = conn.run_commands(cmd)
        print " result: " + str(out)
    elif action == 'del':
        cmd = ['configure terminal','no vlan ' + str(vlan_id),'write memory']
        out = conn.run_commands(cmd)
        print " result: " + str(out)

if __name__ == "__main__":
    main()

