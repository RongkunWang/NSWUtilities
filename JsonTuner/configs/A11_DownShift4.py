#/usr/bin/env python3

ROFFSET = 127
LOFFSET = 128
TPOFFSET = 87
TPINPUTOFFSET = 4
TPINPUTPHASE  = 6

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
