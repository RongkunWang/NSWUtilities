#!/usr/bin/env python3
"""
hard-coded implementation of setting 
"""
#  from __future__ import print_function
#  from __future__ import division
#  from __future__ import absolute_import


from NSWConfigJSONEncoder import NSWConfigJSONEncoder

import argparse
class CustomFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

parser = argparse.ArgumentParser(description='Switch gbtx setup.', formatter_class = CustomFormatter)
parser.add_argument("-i", "--input", 
        type = str,
        help = "the input json to grab configuration from.")
parser.add_argument("-o", "--output", 
        type = str,
        help = "the output json.")
options = parser.parse_args()

import sys, os
from importlib import import_module
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


import json
import copy



raw_data = {}
data = {}
with open(options.input) as fin:
    data = json.load(fin)
    fin.close()

raw_data = copy.deepcopy(data)
for bd, val in raw_data.items():
    if bd == "MMTP" or bd == "STGCTP":
        data["TPCarrier"] = {}
        d = data["TPCarrier"]
        d["OpcServerIp"] = val["OpcServerIp"]
        d["OpcNodeId"]   = val["OpcNodeId"][:-1] + "1"
        d["RJOutSelMM"]  = True
        break

with open(options.output, 'w') as fp:
    tmp2 = json.dump(data, 
            fp, 
            indent=4, 
            sort_keys = False,
            cls=NSWConfigJSONEncoder)
    fp.close()
