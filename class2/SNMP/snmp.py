#!/home/arudas/venv/bin/python

import snmp_helper

def main():
    i = ()
    OID = ''
    ip = "50.76.53.27"
    rtr1_snmp_port=7961
    rtr2_snmp_port=8061
    community_string = "galileo"

    rtr1 = (ip,community_string,rtr1_snmp_port)
    rtr2 = (ip,community_string,rtr2_snmp_port)

    devices = [rtr1, rtr2]

    OID = {
            "sysName" : '1.3.6.1.2.1.1.5.0',
            "sysDescr" : '1.3.6.1.2.1.1.1.0'
        }
    
    
    for i in devices:
        for key in OID:
            print "\nFor device IP: " + i[0] + " port " + str(i[2])
            print "Requested OID: " + str(OID[key]) 
            raw_snmp = get_data(i,OID[key])
            clean_snmp = parse_data(raw_snmp)
            print "" + str(key) + ": \n" + str(clean_snmp)

def get_data(device,oid_req):
    return snmp_helper.snmp_get_oid(device,oid_req)

def parse_data(raw_snmp):
    return snmp_helper.snmp_extract(raw_snmp)

if __name__ == "__main__":
    main()



