#!/usr/bin/env python

from __future__ import division
import math


ASCII_repre = [
        "_a",
        "_b",
        "_c",
        "_d",
        ]

def ebase(l_tup):
    # calculate the elink base(before you add +8, etc
    # l_tup consists of [flxid, logic card, link]
    # if link >= 12, automatically add one for card
    # so (2, 12) do exist, actually represent (3, 0)
    return l_tup[0] * 2 ** 16 + \
            (l_tup[1] + math.floor(l_tup[2] / 12)) * 2 ** 11 + \
            (l_tup[2] % 12) * 2 ** 6

def func(d_opt, boards = {}):
    if boards != {}:
        print "using overwritten \"boards\" setting"
        d_opt["boards"] = boards
    detid_central_value = 46080 # for A14 sFEB
    # each sector,   add 1024  for offset!
    dff_sec = (d_opt["sector"] - 14) * 2 ** 10
    # each quad,    add 8   for offset!
    # each layer,   add 128 for offset!
    # sFEB to pFEB, subtract 2^15 for offset!
    detid_sector = detid_central_value + dff_sec

    for brd, l_links in d_opt["boards"]:
        """
        """
        layer = 0
        if   "IP_L2Q" in brd: layer = 1
        elif "IP_L3Q" in brd: layer = 2
        elif "IP_L4Q" in brd: layer = 3
        elif "HO_L1Q" in brd: layer = 4
        elif "HO_L2Q" in brd: layer = 5
        elif "HO_L3Q" in brd: layer = 6
        elif "HO_L4Q" in brd: layer = 7
        dff_bd = (0 if "sFEB" in brd else (- 2 ** 15)) + layer * 128
        for quad in range(3):
            detid_noGroup = detid_sector + dff_bd + quad * 8
            d_opt["quad"] = quad + 1
            l_grp = [0]
            l_elinks = []
            if d_opt["type"] == "phase1":
                if  quad == 0 and "sFEB" in brd:
                    l_grp = range(2)
                    l_elinks = [ 
                            ebase(l_links[0]) + 8,
                            ebase(l_links[0]) + 16,
                            ]
                elif  quad == 0 and "pFEB" in brd:
                    l_grp = range(2)
                    l_elinks = [ 
                            ebase(l_links[0]) + 8,
                            ebase(l_links[0]) + 16,
                            ]
                elif quad == 1:
                    l_elinks = [ebase(l_links[0]) + 24]
                elif quad == 2:
                    l_elinks = [ebase(l_links[0]) + 33]
            elif d_opt["type"] == "phase1-320":
                if  quad == 0:
                    l_grp = range(2)
                    l_elinks = [ 
                            ebase(l_links[0]) + 9,
                            ebase(l_links[0]) + 17,
                            ]
                elif quad == 1:
                    l_elinks = [ebase(l_links[0]) + 25]
                elif quad == 2:
                    l_elinks = [ebase(l_links[0]) + 33]
            elif d_opt["type"] == "phase1-gbtx2":
                if  quad == 0 and "sFEB" in brd:
                    l_grp = range(4)
                    l_elinks = [ 
                            ebase(l_links[0]) + 8,
                            ebase(l_links[0]) + 16,
                            ebase(l_links[1]) + 8,
                            ebase(l_links[1]) + 16,
                            ]
                elif quad == 0 and "pFEB" in brd:
                    l_grp = range(2)
                    l_elinks = [ 
                            ebase(l_links[0]) + 8,
                            ebase(l_links[0]) + 16,
                            ]
                elif quad == 1:
                    l_grp = range(len(l_links))
                    for link in l_links:
                        l_elinks += [ebase(link) + 24]
                elif quad == 2:
                    l_grp = range(len(l_links))
                    for link in l_links:
                        l_elinks += [ebase(link) + 33]
            # should be absolute, do not use
            elif d_opt["type"] == "phase2-gbtx2-onlyQ1s":
                if  quad == 0 and "sFEB" in brd:
                    l_grp = range(4)
                    l_elinks = [ 
                            ebase(l_links[0]) + 11,
                            ebase(l_links[0]) + 19,
                            ebase(l_links[1]) + 11,
                            ebase(l_links[1]) + 19,
                            ]
                else:
                    l_grp = []
                    continue
            elif d_opt["type"] == "phase2-640":
                if  quad == 0 and "sFEB" in brd:
                    l_grp = range(4)
                    l_elinks = [ 
                            ebase(l_links[0]) + 11,
                            ebase(l_links[0]) + 19,
                            ebase(l_links[1]) + 11,
                            ebase(l_links[1]) + 19,
                            ]
                elif  quad == 0 and "pFEB" in brd:
                    l_grp = range(2)
                    l_elinks = [ 
                            ebase(l_links[0]) + 11,
                            ebase(l_links[0]) + 19,
                            ]
                elif  quad == 1:
                    l_grp = range(len(l_links))
                    for link in l_links:
                        l_elinks += [ebase(link) + 27]
                elif  quad == 2:
                    l_grp = range(len(l_links))
                    for link in l_links:
                        l_elinks += [ebase(link) + 35]
                else:
                    l_grp = []
                    continue

            for grp, elink in zip(l_grp, l_elinks):
                print '<obj class="SwRodInputLink" id="{0}{1}">'.format(
                        brd.format(**d_opt),
                        ASCII_repre[grp] if len(l_grp) > 1 else "")
                print '  <attr name="FelixId" type="u64" val="{0:.0f}"/>'.format(elink)
                print '  <attr name="DetectorId" type="u64" val="{0:.0f}"/>'.format(detid_noGroup + grp)
                print '  <attr name="DetectorName" type="string" val="NSW/L1A/sTGC/{0}/{1}{2}/L{3}/R{4}/G{5}"/>'.format(
                        "strip" if ("sFEB" in brd) else "pad",
                        d_opt["side"], d_opt["sector"],
                        layer,
                        quad,
                        grp)
                print '</obj>'
                print


            pass # quad
        print '<!---                    separation                    -->' 
        pass # board
    pass # function

            #  <obj class="SwRodInputLink" id="A14IP_L1Q1sFEB_a">
            #  <attr name="FelixId" type="u64" val="65547"/>
            #  


# baseline
flxid = 5

sTGC_boards_191 = [
            # name pattern, card and link for gbtx1 (gbtx2 if there is):
            ("{side}{sector}IP_L1Q{quad}sFEB", [(flxid, 0, 0),  (flxid, 2, 12)]), 
            ("{side}{sector}IP_L1Q{quad}pFEB", [(flxid, 0, 6)]), 
            ("{side}{sector}IP_L2Q{quad}sFEB", [(flxid, 0, 7),  (flxid, 2, 18)]), 
            ("{side}{sector}IP_L2Q{quad}pFEB", [(flxid, 0, 1)]), 
            ("{side}{sector}IP_L3Q{quad}sFEB", [(flxid, 0, 2),  (flxid, 2, 13)]), 
            ("{side}{sector}IP_L3Q{quad}pFEB", [(flxid, 0, 8)]), 
            ("{side}{sector}IP_L4Q{quad}sFEB", [(flxid, 0, 9),  (flxid, 2, 19)]), 
            ("{side}{sector}IP_L4Q{quad}pFEB", [(flxid, 0, 3)]), 
            ("{side}{sector}HO_L1Q{quad}sFEB", [(flxid, 0, 4),  (flxid, 2, 14)]), 
            ("{side}{sector}HO_L1Q{quad}pFEB", [(flxid, 0, 10)]), 
            ("{side}{sector}HO_L2Q{quad}sFEB", [(flxid, 0, 11), (flxid, 2, 20)]), 
            ("{side}{sector}HO_L2Q{quad}pFEB", [(flxid, 0, 5)]), 
            ("{side}{sector}HO_L3Q{quad}sFEB", [(flxid, 0, 18), (flxid, 2, 15)]), 
            ("{side}{sector}HO_L3Q{quad}pFEB", [(flxid, 0, 21)]), 
            ("{side}{sector}HO_L4Q{quad}sFEB", [(flxid, 0, 22), (flxid, 2, 21)]), 
            ("{side}{sector}HO_L4Q{quad}pFEB", [(flxid, 0, 19)]), 
            ]

flxid = 0
sTGC_boards_VS = [
            ("{side}{sector}IP_L1Q{quad}pFEB", [(flxid, 0, 12)]), 
            ("{side}{sector}IP_L1Q{quad}sFEB", [(flxid, 0, 13),  (flxid, 0, 14)]), 
            ("{side}{sector}IP_L2Q{quad}pFEB", [(flxid, 0, 15)]), 
            ("{side}{sector}IP_L2Q{quad}sFEB", [(flxid, 0, 16),  (flxid, 0, 17)]), 
            ("{side}{sector}IP_L3Q{quad}pFEB", [(flxid, 0, 18)]), 
            ("{side}{sector}IP_L3Q{quad}sFEB", [(flxid, 0, 19),  (flxid, 0, 20)]), 
            ("{side}{sector}IP_L4Q{quad}pFEB", [(flxid, 0, 21)]), 
            ("{side}{sector}IP_L4Q{quad}sFEB", [(flxid, 0, 22),  (flxid, 0, 23)]), 
        ]

d_opt = {
        "side":    "A",
        "sector":  10,
        #  "type" : "phase1",
        "type" : "phase1-320", # should be used, more modern
        #  "type" : "phase1-gbtx2",
        #  "type" : "phase2-640", 
        #  "type" : "phase2-gbtx2-onlyQ1s",
        "boards": sTGC_boards_191
        }

# 191
func(d_opt)
# VS
#  func(d_opt, sTGC_boards_VS)
