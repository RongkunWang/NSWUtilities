#!/usr/bin/env python
"""
hard-coded implementation of setting 
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse
parser = argparse.ArgumentParser(description='Switch gbtx setup.')
parser.add_argument("-i", "--input", 
        type = str,
        help = "the input json to grab configuration from.")
parser.add_argument("-o", "--output", 
        type = str,
        help = "the output json.")
parser.add_argument("-s", "--setup", 
        type = str,
        default = "sTGC_GBTx2_320",
        help = "the configuration you want to apply, currently support\n"\
        "1. sTGC_GBTx2_320")
options = parser.parse_args()

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from JsonTuner.utils.BoardObj import BoardObj
import JsonTuner.tests.test_module as tm

dict_apply_summary = {
"nothing": {},
"sTGC_GBTx2_320": {
    ("SFEB", "Q1"):{
        "rocCoreDigital":{
            "reg001elinkSpeed":{
                "sroc0":3,
                "sroc1":3,
                "sroc2":2,
                "sroc3":2,
                }, 
            "reg002sRoc0VmmConnections":{
                "vmm0": 1,
                "vmm1": 1,
                "vmm2": 0,
                "vmm3": 0,
                "vmm4": 0,
                "vmm5": 0,
                "vmm6": 0,
                "vmm7": 0
                },
            "reg003sRoc1VmmConnections":{
                "vmm0": 0,
                "vmm1": 0,
                "vmm2": 0,
                "vmm3": 0,
                "vmm4": 1,
                "vmm5": 1,
                "vmm6": 0,
                "vmm7": 0
                },
            "reg004sRoc2VmmConnections":{
                "vmm0": 0,
                "vmm1": 0,
                "vmm2": 1,
                "vmm3": 1,
                "vmm4": 0,
                "vmm5": 0,
                "vmm6": 0,
                "vmm7": 0
                },
            "reg005sRoc3VmmConnections":{
                "vmm0": 0,
                "vmm1": 0,
                "vmm2": 0,
                "vmm3": 0,
                "vmm4": 0,
                "vmm5": 0,
                "vmm6": 1,
                "vmm7": 1
                },
            },
        }, 
    ("SFEB", "Q2"):{
            "rocCoreDigital":{
                "reg001elinkSpeed":{
                    "sroc0":2,
                    "sroc1":2,
                    "sroc2":2,
                    "sroc3":2,
                    },
                "reg002sRoc0VmmConnections":{
                    "vmm0": 1,
                    "vmm1": 1,
                    "vmm2": 1,
                    "vmm3": 1,
                    "vmm4": 0,
                    "vmm5": 0,
                    "vmm6": 0,
                    "vmm7": 0
                    },
                "reg003sRoc1VmmConnections":{
                    "vmm0": 0,
                    "vmm1": 0,
                    "vmm2": 0,
                    "vmm3": 0,
                    "vmm4": 0,
                    "vmm5": 0,
                    "vmm6": 0,
                    "vmm7": 0
                    },
                "reg004sRoc2VmmConnections":{
                    "vmm0": 0, 
                    "vmm1": 0, 
                    "vmm2": 0, 
                    "vmm3": 0, 
                    "vmm4": 1,
                    "vmm5": 1,
                    "vmm6": 1, 
                    "vmm7": 1 
                    },
                "reg005sRoc3VmmConnections":{ 
                    "vmm0": 0, 
                    "vmm1": 0, 
                    "vmm2": 0, 
                    "vmm3": 0, 
                    "vmm4": 0,
                    "vmm5": 0,
                    "vmm6": 0, 
                    "vmm7": 0 
                    },
                },
            },
    ("SFEB", "Q3"):{
            "rocCoreDigital":{
                "reg001elinkSpeed":{
                    "sroc0":1,
                    "sroc1":1,
                    "sroc2":1,
                    "sroc3":1,
                    },
                "reg002sRoc0VmmConnections":{ 
                    "vmm0": 1, 
                    "vmm1": 1, 
                    "vmm2": 1, 
                    "vmm3": 1, 
                    "vmm4": 0,
                    "vmm5": 0,
                    "vmm6": 0, 
                    "vmm7": 0 
                    },
                "reg003sRoc1VmmConnections":{ 
                    "vmm0": 0, 
                    "vmm1": 0, 
                    "vmm2": 0, 
                    "vmm3": 0, 
                    "vmm4": 0,
                    "vmm5": 0,
                    "vmm6": 0, 
                    "vmm7": 0 
                    },
                "reg004sRoc2VmmConnections":{ 
                    "vmm0": 0, 
                    "vmm1": 0, 
                    "vmm2": 0, 
                    "vmm3": 0, 
                    "vmm4": 1,
                    "vmm5": 1,
                    "vmm6": 1, 
                    "vmm7": 1 
                    },
                "reg005sRoc3VmmConnections":{ 
                    "vmm0": 0, 
                    "vmm1": 0, 
                    "vmm2": 0, 
                    "vmm3": 0, 
                    "vmm4": 0,
                    "vmm5": 0,
                    "vmm6": 0, 
                    "vmm7": 0 
                    },
                },
            },
        }, 
    }



if __name__ == "__main__":
    # TODO: replace with arg
    #  confs = "JsonTuner/tests/json/STGC_191_A14_HOIP_TestPulseFinal.json"
    #  output = "replaced_gbtx2.json"
    #  setup = "sTGC_GBTx2_320"



    conf = BoardObj(options.input)
    for bd in conf.boards:
        for board_key, dict_apply in dict_apply_summary[options.setup].items():
            switch = True
            for key in board_key:
                if key not in bd:
                    switch = False
                    break
                pass # loop over all keywords
            if switch:
                conf.apply_one_board(bd, dict_apply)
                break
            pass # loop over settings, see if this apply this board
        pass # loop over boards
    conf.dump(options.output)
