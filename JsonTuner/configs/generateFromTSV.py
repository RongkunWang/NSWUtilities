#!/usr/bin/env python3

template_special = """
ROFFSET       = {ROFFSET}
LOFFSET       = {LOFFSET}
TPOFFSET      = {TPOFFSET}
TPINPUTOFFSET = {TPINPUTOFFSET}
TPINPUTPHASE  = {TPINPUTPHASE}
"""

template_common = """
configs = { 
        ("art_common_config", ):{
            "art_core":{
                "13":{
                    "cfg_bcid0[7:0]": ROFFSET,
                    },
                },
            },
        ("MMTP", ):{
            "gloSyncBcidOffset": TPOFFSET,
            "GlobalInputOffset": TPINPUTOFFSET,
            "GlobalInputPhase":  TPINPUTPHASE,
            }
        }


if ROFFSET != LOFFSET:
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
            """

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

for i, sector in enumerate(fullDict["Sector"]):
    dInit = {}
    for f in fields:
        dInit[f] = fullDict[f][i]
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

