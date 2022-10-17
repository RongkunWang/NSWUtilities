#!/usr/bin/env python3
"""
hard-coded implementation of setting 
"""
#  from __future__ import print_function
#  from __future__ import division
#  from __future__ import absolute_import

from NSWConfigJSONEncoder import NSWConfigJSONEncoder

list_arg = [
        "MMG_Trigger",
        "sTGC_all320",
        "sTGC_GBTx2_320",
        "sTGC_pQ1_split",
        "sTGC_640",
        "sTGC_SFEB6_roc",
        ]

for side in ["A", "C"]:
    for sector in range(1, 17):
        list_arg.append(f"{side}{sector:02d}")

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
parser.add_argument("-s", "--setup", 
        type = str,
        default = "sTGC_GBTx2_320",
        help = "the configuration you want to apply. You can have multiple application, segmented by comma \",\" . currently support\n" +\
        "".join("    {0}. {1}\n".format(i, name) for i, name in enumerate(list_arg)) 
        )
options = parser.parse_args()

import sys, os
from importlib import import_module
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import JsonTuner

import json
from JsonTuner.utils.JsonModules import merge_dict
from JsonTuner.utils.JsonModules import modify_dict
import copy

dict_apply_summary = { }
dict_modify_summary = {}

for name in list_arg:
    import_module("." + name, package="JsonTuner.configs")
    dict_apply_summary[name] = getattr(JsonTuner.configs, name).configs
    try:
        dict_modify_summary[name] = getattr(JsonTuner.configs, name).configsModify
    except:
        dict_modify_summary[name] = {}
        pass
    pass

#  print(dict_apply_summary["MMG_Trigger"])
#  print(dict_modify_summary["MMG_Trigger"])

raw_data = {}
with open(options.input) as fin:
    raw_data = json.load(fin)
    fin.close()

data = copy.deepcopy(raw_data)

for bd, val in raw_data.items():
    for board_key, dict_apply in dict_modify_summary[options.setup].items():
        switch = True
        for key in board_key:
            if "|" in key:
                list_of_or = key.split("|")
                switch = False
                for key_in_one_or in list_of_or:
                    if key_in_one_or in bd:
                        switch = True
                        break
                    pass
                if not switch:
                    break
            else:
                if key not in bd:
                    switch = False
                    break
            pass # loop over all keywords for matching
        if switch:
            data[bd] = modify_dict(dict_apply, val)
        pass
raw_data = copy.deepcopy(data)

for bd, val in raw_data.items():
    for board_key, dict_apply in dict_apply_summary[options.setup].items():
        switch = True
        for key in board_key:
            if "|" in key:
                list_of_or = key.split("|")
                switch = False
                for key_in_one_or in list_of_or:
                    if key_in_one_or in bd:
                        switch = True
                        break
                    pass
                if not switch:
                    break
            else:
                if key not in bd:
                    switch = False
                    break
            pass # loop over all keywords for matching
        if switch:
            data[bd] = merge_dict(dict_apply, val)
            pass
        pass # loop over settings, see if this apply this board
    pass # loop over boards in json

with open(options.output, 'w') as fp:
    tmp2 = json.dump(data, 
            fp, 
            indent=4, 
            sort_keys = False,
            cls=NSWConfigJSONEncoder)
    fp.close()
