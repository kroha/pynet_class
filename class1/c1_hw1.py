#!/usr/bin/python

from pprint import pprint as pp
import yaml
import json
from ciscoconfparse import CiscoConfParse

# Define variable
list = range (20)
dir = {
    "first"     : "element 1",
    "second"    : "element 2"
    }

list.append(dir)

# yaml/json 
# create file json:

print("Initial list $list")

def create_json_file(list):
    with open("c1_file.json", "w") as f:
        json.dump(list, f)
        print "\n\nJSON file written."


def create_yaml_file(list):
    with open("c1_file.yaml", "w") as f:
        f.write(yaml.dump(list, default_flow_style = True))
        print "\n\nYAML file written."

def open_json_file():
    new_list = []
    with open("c1_file.json") as f:
        new_list=json.load(f)
        print "\n\nJSON file read"
        pp(new_list)

def open_yaml_file():
    new_list = []
    with open("c1_file.yaml") as f:
        new_list=yaml.load(f)
        print "\n\nYAML file print:"
        pp(new_list)

def cisco_conf_task_1():
    print "\n\nCisco parse exersise 1.\n"
    cfg_file = CiscoConfParse("cisco_ipsec.txt")
    c_maps = cfg_file.find_objects(r"^crypto map CRYPTO")
    x = 1
    y = 1
    for element in c_maps:
        print "Crypto map %s cfg: %s" % (x , element.text)
        x +=1
        y = 1
        for subelement in element.children:
            print "  line %s: %s" % (y, subelement.text)
            y += 1
            
def cisco_conf_task_2():
    print "\n\nCisco parse exersise 2.\n"
    cfg_file = CiscoConfParse("cisco_ipsec.txt")
    c_maps = cfg_file.find_parents_w_child("^crypto map CRYPTO","^ set pfs group2")
    x = 1
    for element in c_maps:
        print "entry # %s that are using PFS group2:  %s" % (x, element)
        x += 1
        
def cisco_conf_task_3():
    print "\n\nCisco parse exersise 3.\n"
    cfg_file = CiscoConfParse("cisco_ipsec.txt")
    c_maps = cfg_file.find_parents_wo_child("^crypto map CRYPTO","^ set transform-set AES")
    x = 1
    for element in c_maps:
        print "entry # %s that are using PFS group2:  %s" % (x, element)
        x += 1

create_json_file(list)
create_yaml_file(list)
open_json_file()
open_yaml_file()
cisco_conf_task_1()
cisco_conf_task_2()
cisco_conf_task_3()
