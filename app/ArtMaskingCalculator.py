#!/usr/bin/env python

"""
A script to convert from <MMFE8_name,vmmid> to ADDC_name,art,register,value
to manually mask
"""

import argparse
import re

def name_encoder(d):
    """
    input:  {layer, PCB, ML, side} or {Glayer, radius)
    output:  legit ConfigName
    """
    try:
        d["PCB"] = d["radius"] // 2 + 1
        if d["Glayer"] >= 4:
            d["ML"] = "HO"
            d["side"] = "R"
            d["layer"] = 8 - d["Glayer"]
        else:
            d["ML"] = "IP"
            d["side"] = "L"
            d["layer"] = d["Glayer"] + 1
        # reverse of below
        residual = d["radius"] - (d["layer"] % 2) - (d["PCB"] - 1) * 2
        if residual == 0:
            d["side"] = "L" if d["side"] == "R" else "R"
    except:
        pass
    return "MMFE8_L{layer}P{PCB}_{ML}{side}".format(**d)

def name_decoder(name):
    """
    input: legit ConfigName, 
    output: {layer, PCB, ML, side}
    """
    l = name.split("_")
    d = {}
    d["layer"] = int(l[1][1])
    d["PCB"]   = int(l[1][3])
    d["ML"]    = l[2][:2]
    d["side"]  = l[2][-1]

    if l[2] in ["HOR", "IPL"]:
        d["radius"] = (d["PCB"] - 1) * 2 + (d["layer"] % 2) - 1
    else:
        d["radius"] = (d["PCB"] - 1) * 2 + (d["layer"] % 2)
        pass
    return d

def addc_retriever(name): 
    """
    input: legit ConfigName
    output: ConfigName of the ADDC
    """
    d = name_decoder(name)
    layer = 1
    PCB = 3
    if d["layer"] in [3, 4]:
        layer = 4
    if d["radius"] % 2 == 1:
        PCB = 6
    return "ADDC_L{0}P{1}_{2}{3}".format(layer, PCB, d["ML"], d["side"])

def art_retriever(name):
    """
    input: legit ConfigName
    output: (art index, FE index)
    """
    d = name_decoder(name)
    reverse = True
    if d["layer"] in [1, 2] and d["ML"] == "IP" and d["side"] == "R":
        reverse = False
    if d["layer"] in [3, 4] and d["ML"] == "IP" and d["side"] == "L":
        reverse = False
    if d["layer"] in [3, 4] and d["ML"] == "HO" and d["side"] == "R":
        reverse = False
    if d["layer"] in [1, 2] and d["ML"] == "HO" and d["side"] == "L":
        reverse = False
    FE = d["PCB"] - 1
    if reverse:
        FE = 7 - FE
    return (FE // 4, FE)

def art_register_mask(name, vmmid):
    addc = addc_retriever(name)
    art, FE = art_retriever(name)
    register = 9 +  FE % 4
    value = 2 ** int(vmmid)
    return (addc, art, register, value)

def name_reguarlizer(name):
    """
    handles the checking of ConfigName of boards
    """
    l = name.split("_")
    if len(l) != 3 or l[0] != "MMFE8": raise ValueError("Board name must have MMFE8_LXPX_YYZ or be MLXPXYYZ")
    if len(l[1]) != 4: raise ValueError("Board name must have 4 characters in the center position" )
    if l[1][0] != "L": raise ValueError("Missing L in your board name, format: ?????_L???_???")
    if l[1][2] != "P": raise ValueError("Missing P in your board name, format: ?????_??P?_???")
    if int(l[1][1]) < 1 or int(l[1][1]) > 4: raise ValueError("layer must be from 1 to 4")
    if int(l[1][3]) < 1 or int(l[1][3]) > 8: raise ValueError("PCB must be from 1 to 8")
    if len(l[2]) != 3: raise ValueError("Board name must have 3 characters in the right position" )
    if l[2][:2] not in ["HO", "IP"]: raise ValueError("Chamber name must be IP or HO")
    if l[2][2] not in ["L", "R"]: raise ValueError("Side must be L or R")
    return name

def name_converter(name):
    """
    currently receives two types of input:
        1. pass in MMFE8_LXPX_YYZ (ConfigName)
        2. pass in MLXPXYYZ (Trigger Plot Name), we can convert it to MMFE8_LXPX_YYZ
        3. pass in MMFE8_LXRX (global name) here R: 0..15, L: 0..7
    """
    # Config pattern
    if re.match("^MMFE8_L[1-4]P[1-8]_(IP|HO)(R|L)$", name):
        return name_reguarlizer(name)
    if re.match("^ML[1-4]P[1-8](IP|HO)(R|L)$", name):
        return name_reguarlizer("MMFE8_" + name[1:5] + "_" + name[-3:])
    m = re.match("^MMFE8_L([0-7])R([0-9]|1[0-5])$", name)
    if m:
        d = {}
        d["Glayer"]  = int(m.group(1))
        d["radius"] = int(m.group(2))
        return name_reguarlizer(name_encoder(d))
    raise ValueError("Please look at __doc__ of name_converter()")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            usage=__doc__, formatter_class=argparse.RawTextHelpFormatter
            )
    parser.add_argument("-b", "--board", dest="boards",
            help="pass in board,vmmid and the ADDC,art,register,value will be returned.",
            required=True,
            nargs="+")
    parser.add_argument("-a", "--art", dest="type", action="store_const",
            const = "ArtMask")
    parser.add_argument("-d", "--decode", dest="type", action="store_const",
            const = "SimpleDecode")

    opts = parser.parse_args()
    iterators = None
    try:
        iterators = list(map(lambda x: x.split(","), opts.boards))
    except ValueError:
        raise ValueError("must pass in <MMFE8_name,vmmid>")
    for name, vmmid in iterators:
        brd_name = name_converter(name)
        print(brd_name)
        if opts.type == "ArtMask":
            print(art_register_mask(brd_name, vmmid))
        if opts.type == "SimpleDecode":
            print(name_decoder(brd_name))
    pass
