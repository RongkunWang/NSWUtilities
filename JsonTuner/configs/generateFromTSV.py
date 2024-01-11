#!/usr/bin/env python3

template_special = """
ROFFSET       = {ROFFSET}
LOFFSET       = {LOFFSET}
TPOFFSET      = {TPOFFSET(gloSyncBcidOffset)}
SEGMENTADJUST      = {SegmentAdjust}
TPINPUTPHASE  = {GlobalInputPhase}
TPINPUTOFFSET = {GlobalInputOffset}
TPINPUTL1PHASE   = {gbtL1ddPhaseOffset}
VMMCHOFFSET   = {VMMCHOFFSET}
"""

template_common = """
configs = { 
        #  ("vmm_common_config", ):{
            #  "offset": VMMCHOFFSET
            #  },
        ("art_common_config", ):{
            "art_core":{
                "13":{
                    "cfg_bcid0[7:0]": ROFFSET,
                    },
                },
            },
        ("MMTP", ):{
            "gloSyncBcidOffset": TPOFFSET,
            "SegmentAdjust": SEGMENTADJUST,
            "GlobalInputOffset": TPINPUTOFFSET,
            "GlobalInputPhase":  TPINPUTPHASE,
            "gbtL1ddPhaseOffset": TPINPUTL1PHASE,
            }
        }


if ROFFSET != LOFFSET:
    #  configs[ ("ADDC", "L0/E|L1/O|L2/E|L3/O|L4/E|L5/O|L6/E|L7/O")] = {
    configs[ ("ADDC", "HOL|IPL")] = {
            "art0" : {
                "art_core":{
                    "13":{
                        "cfg_bcid0[7:0]": LOFFSET,
                        },
                    },
                },
            "art1" : {
                "art_core":{
                    "13":{
                        "cfg_bcid0[7:0]": LOFFSET,
                        },
                    },
                },
            }
else:
    configs[ ("ADDC", "HOL|IPL")] = {
            "art0": {
                "art_core":{}
                },
            "art1": {
                "art_core":{}
                }
    }
            """

offset_A = [
        136,
        136,
        136,
        136,
        136,
        136,

        135,
        135,
        135,
        135,

        136,
        136,
        136,
        136,
        136,
        136,
        ]
offset_C = [
        136,
        136,
        136,
        136,
        136,

        135,
        135,
        135,
        135,
        135,

        136,
        135,
        136,
        136,
        136,
        136,
        ]

l_offset = offset_A + offset_C

ifile = open("summary.tsv")
fields = []
fullDict = {}
for line in ifile:
    row_list = line.split()
    # initialize
    if len(fields) == 0:
        for s in row_list:
            fullDict[s] = []
            fields.append(s)
            pass
        continue

    for i, s in enumerate(row_list):
        fullDict[fields[i]].append(s)

print(len(fullDict["Sector"]), fullDict["Sector"])
for i, sector in enumerate(fullDict["Sector"]):
    dInit = {}
    for f in fields:
        #  print(f, len(fullDict[f]))
        dInit[f] = fullDict[f][i]
    dInit["VMMCHOFFSET"] = l_offset[i] + 4 # add four for moving from 200ns to 100ns!
    print(dInit)
    with open(f"{fullDict['Sector'][i]}_auto.py", 'w') as oFile:
        oFile.write(template_special.format(**dInit))
        oFile.write(template_common)
        oFile.close()
#  for side in ["A", "C"]:
    #  for sec in range(1, 17):
        #  sector = f"{side}{sec:02d}"
        #  print(sector)
        #  os.system(f"cat ${sector}.py | awk ''")
        #  cat ${word}.py | awk -v d=4 '/ROFFSET[[:space:]]*=/{$3-=d}1' | \
            #  awk -v d=4 '/LOFFSET[[:space:]]*=/{$3-=d}1' | \
            #  awk -v d=4 '/TPOFFSET[[:space:]]*=/{$3-=d}1' > ${word}_DownShift4.py

