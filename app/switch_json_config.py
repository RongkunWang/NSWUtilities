#!/usr/bin/env python3
"""
hard-coded implementation of setting 
"""
#  from __future__ import print_function
#  from __future__ import division
#  from __future__ import absolute_import

list_arg = [
        "MMG_Trigger",
        "sTGC_all320",
        "sTGC_GBTx2_320",
        "sTGC_pQ1_split",
        "sTGC_640",
        "sTGC_SFEB6_roc",
        ]

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

#  import JsonTuner.configs.sTGC_640
#  import JsonTuner.configs.sTGC_GBTx2_320
#  import JsonTuner.configs.sTGC_pQ1_split

import JsonTuner

dict_apply_summary = {
    "nothing": {},
    #  "sTGC_640": JsonTuner.configs.sTGC_640.configs,
    #  "sTGC_GBTx2_320": JsonTuner.configs.sTGC_GBTx2_320.configs,
    #  "sTGC_pQ1_split": JsonTuner.configs.sTGC_pQ1_split.configs,
    }

for name in list_arg:
    import_module("." + name, package="JsonTuner.configs")
    dict_apply_summary[name] = getattr(JsonTuner.configs, name).configs

from JsonTuner.utils.BoardObj import BoardObj



if __name__ == "__main__":
    # TODO: replace with arg
    #  confs = "JsonTuner/tests/json/STGC_191_A14_HOIP_TestPulseFinal.json"
    #  output = "replaced_gbtx2.json"
    #  setup = "sTGC_GBTx2_320"

    this_input = options.input
    for setup in options.setup.split(","):
        conf = BoardObj(this_input)
        for bd in conf.boards:
            for board_key, dict_apply in dict_apply_summary[setup].items():
                switch = True
                for key in board_key:
                    if key not in bd:
                        switch = False
                        break
                    pass # loop over all keywords
                if switch:
                    conf.apply_one_board(bd, dict_apply)
                    continue
                pass # loop over settings, see if this apply this board
            pass # loop over boards
        conf.dump(options.output)
        this_input = options.output
