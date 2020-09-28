#!/usr/bin/env python3
# TODO: replace - a selected number of registers (important)
# TODO: diff_dict to summarize the difference

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from collections import OrderedDict

import copy

def is_dict(a):
    return isinstance(a, dict)

def merge_dict(uni, com):
    """ 
    takes two dictionaries uni, com.
    return a dictionary that has all the elements in com,
        with elements from uni when it's different from com
    """
    dout = {}
    for key, value in com.items():
        if key not in uni:
            dout[key] = copy.deepcopy(value)
            continue
        if is_dict(value):
            dout[key] = merge_dict(uni[key], com[key])
            continue
        if key in uni:
            dout[key] = uni[key]
            pass
        pass
    return dout

def diff_dict(first_dict, second_dict):
    """
    takes two dictionaries
    takes only the keys in case of difference, value comes from the first
    assumes they have the same keys (TODO)
    """
    dout = {}
    for key, value in first_dict.items():
        if is_dict(value):
            dtmp = diff_dict(first_dict[key], second_dict[key])
            if dtmp != {}:
                dout[key] = dtmp
            continue
        if value == second_dict[key]:
            continue
        dout[key] = value
    return dout

def sort_dict(dic):
    #  print (dic, "\n")
    dout = dic.copy() 
    for key, value in dic.items():
        #  print(value)
        if is_dict(value):
            dout[key] = sort_dict(value)
        pass
    return OrderedDict(sorted(dout.items()))


if __name__ == "__main__":
    print ("Doing some basic test!")

    import json

    commonS = '{"error":"222", "error_3":{"c":"ddd", "b":"333"}}'
    boardS  = '{"error":"111", "error_3":{"c":"eee"}}'

    common = json.loads(commonS)
    board  = json.loads(boardS)

    print ("common", common)
    print ("board", board)
    print (merge_dict(board, common))

    #  print


    #  for i in common:
        #  print common[i]
