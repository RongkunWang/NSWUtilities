#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from ..utils.BoardObj import BoardObj
from ..utils import JsonModules as JM
import json

# TODO: write test suite from unittest
# https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

import os

def baseline_obj():
    common = {"error":"222", "error_3":{"c":"ddd", "b":"333"}, "corr":3}
    board  = {"error":"111", "error_3":{"c":"eee", "b":"333"}, "corr":3}
    return common, board


def gbtx1_2_file():
    j1 = BoardObj(os.path.dirname(os.path.abspath(__file__)) + "/json/STGC_191_A14_HOIP_TestPulseFinal.json")
    j2 = BoardObj(os.path.dirname(os.path.abspath(__file__)) + "/json/STGC_191_A14_HOIP_TestPulse_GBTx2.json")
    return j1, j2

def test_dump():
    json_obj1, json_obj2 = gbtx1_2_file()
    json_obj1.debug_print()
    json_obj2.debug_print()
    json_obj1.dump("out1.json")
    json_obj2.dump("out2.json")
    pass

def test_diff():
    j1, j2 = baseline_obj()
    print(JM.diff_dict(j1, j2))
    pass

def test_diff2():
    json_obj1, json_obj2 = gbtx1_2_file()
    with open("diff.json", 'w') as fp: 
        json.dump(
                JM.diff_dict(json_obj2.boards, json_obj1.boards),
                fp, indent=4, sort_keys = True)
    pass

def test_apply():
    j1, j2 = baseline_obj()
    a = JM.merge_dict(
            {"error":"333", "error_3":{"b":"555"}},
            j1, 
            )
    print(a)
    a = JM.merge_dict(
            {"error":"333", "error_3":{"b":"555"}},
            j2, 
            )
    print(a)

if __name__ == "__main__":
    print("This is a test module")
