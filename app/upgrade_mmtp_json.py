#!/usr/bin/env python3

from glob import glob
from NSWConfigJSONEncoder import NSWConfigJSONEncoder
import csv, json
import copy
from pprint import pprint
import sys

with open(sys.argv[1]) as f:
    d = json.load(f)
    mmtp_ori = d["MMTP"]
    mmtp_new = {"Version":2, 
                "ConfigRegisters":[],
                "SkipRegisters":[],
                "OpcNodeId" : mmtp_ori["OpcNodeId"],
                "OpcServerIp" : mmtp_ori["OpcServerIp"],
                }




### 
# process the new MMTP
### 

with open("OldNewRegMap.csv") as f:
    regs = csv.DictReader(f, delimiter=',')
    for r in regs:
        if r["In Json"] != "T": continue

        jname, bname, rname = r["Json Name"], r["Bus Name"], r["Register Name"]
        default = r["c++ Code/Default Value"]
        print(jname, bname, rname)
        mmtp_new["ConfigRegisters"].append(f"\"{bname}.{rname}\"")
        if bname not in mmtp_new:
            mmtp_new[bname] = {}

        if jname != "" and jname in mmtp_ori:
            mmtp_new[bname][rname] = int(mmtp_ori[jname])
        else:
            mmtp_new[bname][rname] = int(default)
        pass

print(mmtp_new)


with open(sys.argv[2], 'w') as f:
    d["MMTP"] = mmtp_new
    json.dump(d, f,
              indent=4,
              sort_keys = False,
              cls=NSWConfigJSONEncoder)
