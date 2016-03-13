#!/usr/bin/python

# Module should be located in the ANSIBLE LIB directory: ./ANSIBLE/library/c7_ansible_module.py

from ansible.module_utils.basic import *
import pyeapi
import pprint
import sys

def main():
    change = False
    module = AnsibleModule(
    argument_spec = dict(
            vlanid=dict(required=True),
            name=dict(required=True),
            sw=dict(required=True)
        )
    )
    vlan_id = module.params['vlanid']
    vlan_name = module.params.get('name')
    sw = module.params['sw']

    conn = pyeapi.connect_to(sw)
    change = run(conn,'add',vlan_id,vlan_name)

    ms = "vlan_id " + str(vlan_id) + " name " + str(vlan_name)
    module.exit_json(msg=ms,changed=change)

def run(conn,action,vlan_id=0, vlan_name='none'):
    if action == 'add':
        change = False
        cmd = ['show vlan id ' + str(vlan_id)]
        cmd2 = ['show vlan name ' + str(vlan_name)]
        try:
            out = conn.run_commands(cmd)
        except pyeapi.eapilib.CommandError:
            cmd = ['configure terminal','vlan ' + str(vlan_id),'name ' + str(vlan_name),'write memory']
            out = conn.run_commands(cmd)
            change = True
            return change
        try:
            out2 = conn.run_commands(cmd2)
        except pyeapi.eapilib.CommandError:
            cmd = ['configure terminal','vlan ' + str(vlan_id),'name ' + str(vlan_name),'write memory']
            out = conn.run_commands(cmd)
            change = True
            return change
        return change

if __name__ == '__main__':
    main()

