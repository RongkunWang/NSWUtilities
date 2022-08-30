#/usr/bin/env python3

configs = { 
    ("art_common_config", ):{
        "art_core":{
            "13":{
                "cfg_bcid0[7:0]": "133",
                },
            "14":{
                "cfg_bcid0[11:8]": "0",                                                                                                                                             
                "cfg_bcid1[3:0]": "11"
                },
            "15": {
                "cfg_bcid1[11:4]": "222"
                },

            },
        },
    ("MMTP", ):{
        "SkipRegisters" : ["33"],
        "gloSyncBcidOffset":"94",
        "gloSyncIdleState":"1"
        }
    }

# TODO could use a functionform..
configsModify = {
    ("MMTP", ):{
        "OpcNodeId": (".I2C_0.bus0", "")
        },
    ("ADDC", ):{
        "art0": {
            "OpcNodeId_TP": (".I2C_0.bus0", "")
            },
        "art1": {
            "OpcNodeId_TP": (".I2C_0.bus0", "")
            },
        }
    }

