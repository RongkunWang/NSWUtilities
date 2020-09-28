#!/usr/bin/env python3
"""
hard-coded implementation of setting 
"""
#  from __future__ import print_function
#  from __future__ import division
#  from __future__ import absolute_import

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
        help = "the configuration you want to apply, currently support\n"\
        "    1. sTGC_GBTx2_320\n"\
        "    2. sTGC_640\n"\
        "    3. sTGC_pQ1_split")
options = parser.parse_args()

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import JsonTuner.configs.sTGC_640
import JsonTuner.configs.sTGC_GBTx2_320
import JsonTuner.configs.sTGC_pQ1_split
from JsonTuner.utils.BoardObj import BoardObj

dict_apply_summary = {
    "nothing": {},
    "sTGC_640": JsonTuner.configs.sTGC_640.configs,
    "sTGC_GBTx2_320": JsonTuner.configs.sTGC_GBTx2_320.configs,
    "sTGC_pQ1_split": JsonTuner.configs.sTGC_pQ1_split.configs,
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
