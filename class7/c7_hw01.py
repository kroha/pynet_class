#!/home/arudas/venv/bin/python

import pyeapi
import pprint


def main():
    conn = pyeapi.connect_to('pynet-sw3')
    out = conn.run_commands("show interfaces")
    for i in out[0]['interfaces']:
        if out[0]['interfaces'][i].has_key('interfaceCounters'):
            print "Interface: " + i + "\n\tinOctets: " + str(out[0]['interfaces'][i]['interfaceCounters']['inOctets'])
            print "\toutOctets: " + str(out[0]['interfaces'][i]['interfaceCounters']['outOctets'])
        else:
            continue

if __name__ == "__main__":
    main()

