#!/usr/bin/env python3
"""
don't forget to source FELIX environment before running!
in um-felix?.cern.ch
    source /opt/felix/setup.sh   for latest rpm build
    source /home/setup/setup.sh  for very old local build

version 2.6 Jul. 2 2020
    add readback for gbtx2
version 2.5 Jul. 2 2020
     timeout bug fix
version 2.4 Apr. 21 2020
    python3 with timeout

version 2.3 Mar. 4  2020
   gbtx2 group0 need to set reg63 as 00

version 2.2 Jan. XX 2020
use I2C from EC channel to config gbtx2 (test)


version 2.1 Oct. 23 2019
add sleep to fix breaking in inspecting dll, 

previous versions: 
    1.0 without train/read
    2.0 add training, preliminary testing successful

Author: Rongkun Wang  <rongkun.wang at cern.ch>
"""

import argparse

parser = argparse.ArgumentParser(description='Config gbtx.')
parser.add_argument("-i", "--init", action = "store_true",
        help = "This will have to be run first to configure gbtx correct!",)
parser.add_argument("-t", "--train", action = "store_true",
        help = "This will have to be run after FE are configured, to train the phases. then we can do static phase setting, in the same directory!",)
parser.add_argument("-s", "--setphase", type=str,
        default = "",
        help = "Manually set the phase, format: group;channel;value",)
parser.add_argument("-r", "--readback", action = "store_true",
        help = "This will read the registers!",)
parser.add_argument("-p", "--printphase", action = "store_true",
        help = "Print out the phases!",)
parser.add_argument("-n", "--not_inspect", action = "store_true",
        help = "This will cause the script not to inspect DLL(brute)!",)
args = parser.parse_args()

import os, sys
sys.path.append("/afs/cern.ch/user/r/rowang/public/MyPythonUtilities")
import MyPythonSystemUtil as mpsu

sys.path.append("/afs/cern.ch/work/r/rowang/public/FELIX/NSWUtilities/")
#  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from GBTxConfig.other_words import *
from GBTxConfig.GBTXConfigHandler import *



############################################
#  don't need to change those above
############################################

# 1st number is fiber number / GBT link number
# 2nd number is which GBTx the fiber is connected to (1/2) on L1DDC (need to change I2C address)
# 3rd number is for GBTx1 is flx-card (0/1 potentiall 2/3) for flx-card device to use
#               for GBTx2 is I2c slave
# 4rd address is used for GBTx2 as the elink address

l_gbtxn = [
        #  (0, 1, 0),
        #  (1, 1, 0),
        #  (3, 1, 0),
        #  (4, 1, 0),
        #  (5, 1, 0),
        #  (6, 1, 0),
        #  (7, 1, 0),
        #  (8, 1, 0),
        #  (9, 1, 0),
        (10, 1, 0),
        #  (11, 1, 0),


        #  (6, 1, 1),
        #  (7, 1, 1),
        #  (8, 1, 1),
        #  (9, 1, 1),
        #  (10, 1, 1),
        ]

# group 0-4 rate selection, subject to flx fmw and technology used
g0_rate = 80
g1_rate = 80
g2_rate = 320
g3_rate = 320
g4_rate = 320

############################################
#  don't need to change those below
############################################

# words go into a gbtx config file
# each word is one byte

# these group0 phase words are gbt ic address specific.
gbt_dict={
        1:words_68_77_gbtx1,
        2:words_68_77_gbtx2
        }

os.system("mkdir -p GBTXconfigs")

l_faulty = []
l_not_locked = []

for arg_tuple in l_gbtxn:
    fiberNo = arg_tuple[0] 
    ICaddr = arg_tuple[1] 
    flx_card = arg_tuple[2] 
    hostname = ""

    if ICaddr == 1:
        g0_rate = 80


    if ICaddr == 2:
        g0_rate = 0
        hostname = arg_tuple[3] 

    # default config
    l_words = [
            words_0_61,
            phase_mode["training"],   
            # 63 inEportCtr1    group0
            dict_rate[g0_rate],
            words_64_67,
            gbt_dict[ICaddr],
            words_78_86,
            # 87 inEportCtr25   group1
            dict_rate[g0_rate],
            words_88_110,
            # 111 inEportCtr49  group2
            dict_rate[g0_rate],
            words_112_134,
            # 135 inEportCtr73  group3
            dict_rate[g0_rate],
            words_136_158,
            # 159 inEportCtr97  group4
            dict_rate[g0_rate],
            words_160_368,
            ]

    con = GBTXConfigHandler("write_list", l_words, 
            flx_card, fiberNo, ICaddr, hostname)
    con.set_MM()
    con.DoOneByOne()
    

    if ICaddr == 2:
        con.SetNoInspect(True)
    else:
        con.SetNoInspect(args.not_inspect)

    #  con.overwrite_dll()

    if  args.init:
        print(mpsu.green("===> upload all config"))
        con.upload_config()
    elif args.readback:
        con.read_config(1)
    elif args.printphase:
        con.print_phase()
    elif args.setphase != "":
        l_arg = args.setphase.split(";")
        l_arg[0] = int(l_arg[0])
        l_arg[1] = int(l_arg[1])
        self.upload_single_phase( *l_arg )
    elif args.train:
        # first upload the very first config with IC
        #  print(mpsu.green("===> upload all config"))
        #  con.upload_config()

        # do the training! or just checking directly!
        if not con.train_phases():
        #  if not con.inspect_lock():
            l_not_locked.append(con.read_file_name)


        # read back config in a file for phases
        if ICaddr == 1:
            con.read_config()
    else:
        l_faulty.append( con.read_phase() )
        con.upload_config()
        pass
    pass

print("\n")
for error in l_faulty:
    if error:
        # None means success
        print(mpsu.TRed("WARNING") + ": file {0} is faulty, please check if there's register values inside! It's very likely you didn't open this elink or you have some felix issue.".format(error))
for error in l_not_locked:
    # None means success
    print(mpsu.TRed("WARNING") + ": training of {0}, the DLL is not locked! Phase readback might not be valid. Search for INSPECT in the terminal for more details".format(error))

# reset the TH_FanOut to none for both cards, 
# this is fail-safe if you didn't lock THFO
os.system("femu -n -d 0")
os.system("femu -n -d 1")
