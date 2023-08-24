#/usr/bin/env python3

configs = { 
        ("MMTP"):{
            #  "ARTWindowCenter" : None,
            #  "ARTWindowLeft" : None,
            #  "ARTWindowRight" : None,
            "L1AOpeningOffset": 33,
            "L1ARequestOffset": 32,
            "L1AClosingOffset": 31,
            "L1ATimeoutWindow": 64,
            "L1ABusyThreshold": 7,
            "LocalBcidOffset": 37,
            #  "gloSyncIdleState": 1,
            #  "latTxBcidOffset": 100,
            #  "SelfTriggerDelay": 0,
            #  "SkipRegisters": [],
            },
        #  ("tp_common_config"):{},
        # 100ns timing at peak
        #  ("vmm_common_config"):{
            #  "sfam": "1",
            #  "st": "1",
            #  },
        }

#  configs = { 
    #  ("art_common_config", ):{
        #  "art_core":{
            #  "13":{
                #  "cfg_bcid0[7:0]": "133",
                #  },
            #  "14":{
                #  "cfg_bcid0[11:8]": "0",                                                                                                                                             
                #  "cfg_bcid1[3:0]": "11"
                #  },
            #  "15": {
                #  "cfg_bcid1[11:4]": "222"
                #  },

            #  },
        #  },
    #  ("MMTP", ):{
        #  "SkipRegisters" : ["33"],
        #  "gloSyncBcidOffset":"94",
        #  "gloSyncIdleState":"1"
        #  }
    #  }

# TODO could use a functionform..
#  configsModify = {
    #  ("MMTP", ):{
        #  "OpcNodeId": (".I2C_0.bus0", "")
        #  },
    #  ("ADDC", ):{
        #  "art0": {
            #  "OpcNodeId_TP": (".I2C_0.bus0", "")
            #  },
        #  "art1": {
            #  "OpcNodeId_TP": (".I2C_0.bus0", "")
            #  },
        #  }
    #  }

