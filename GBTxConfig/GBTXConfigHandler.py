#!/usr/bin/env python3

# mapping for phase decimal to word
#  000000: disabled
#  010101: 80Mb/s
#  101010: 160Mb/s
#  111111: 320Mb/s

# enabling groups
# group0 07 (channel 2 1 0) reg81
# group1 11 (channel 4   0) reg105
# group2 11 (channel 4   0) reg129
# group3 11 (channel 4   0) reg153
# group4 11 (channel 4   0) reg177

import os, time
import subprocess

dict_phase = {
        0:  "00",
        80: "15",
        160:"2a",
        320:"3f", 
        }

# phase aligner mode
phase_mode = {
    "static":"00",
    "training":"15",
    "tracking":"2a",
    "none":"3f",
}

def timeout_run(*arg, **kwargs):
    try:
        # fine tuning
        subprocess.run(*arg, **kwargs, timeout = 3)
    except subprocess.TimeoutExpired:
        print("WARNING! Timeout the process! Shouldn't affect uploaded values")
    except e:
        print("unexpected exception", sys.exc_info()[0])

class GBTXConfigHandler():
    def __init__(self, tp, val, _flx_card, _fiberNo, _ICaddr, hostname=""):
        """
        tp: 
            write_list: val is a list for writing and uploading
            read_file:  val is a file with readback data
        """
        self.reg = []
        self.flx_card = _flx_card
        self.fiberNo  = _fiberNo
        self.ICaddr   = _ICaddr
        self.not_inspect = False
        self.hostname = hostname
        self.do_one_by_one = False
      

        os.system("mkdir -p GBTXconfigs")

        self.write_file_name = "GBTXconfigs/upload_card{0}_link{1}_gbt{2}.txt".format(_flx_card, _fiberNo, _ICaddr)
        self.read_file_name  = "GBTXconfigs/read_card{0}_link{1}_gbt{2}.txt".format(_flx_card, _fiberNo, _ICaddr)
        if tp == "write_list":
            for long_word in val:
                for word in long_word.rstrip().split("\n"):
                    self.reg.append(word)
            self.overwrite_gbtx2()
            #  if self.ICaddr == 2:
                #  # watchdog timer
                #  # 00 means turn off
                #  # if set to 07, turned on, and there is no fiber connected, 
                #  #  it will constantly reset the gbtx, which is what we don't want.
                #  print("Overwritting GBTx2 registers 50, 52, 254 to 00")
                #  self.reg[50] = "00"
                #  self.reg[52] = "00"
                #  self.reg[254] = "00"
            pass
        elif tp == "read_file":
            for line in val:
                if "Reply" not in line:
                    continue
                else:
                    break
            for line in val:
                if "chunks" in line:
                    break
                for word in line.split(":")[1].strip().split(" "):
                    self.reg.append(word)
            pass
        else:
            pass
        pass

    def overwrite_gbtx2(self):
        if self.ICaddr == 2:
            # watchdog timer
            # 00 means turn off
            # if set to 07, turned on, and there is no fiber connected, 
            #  it will constantly reset the gbtx, which is what we don't want.
            self.reg[50] = "00"
            self.reg[52] = "00"
            self.reg[254] = "00"

    def DoOneByOne(self, val = True):
        self.do_one_by_one = val

    def SetNoInspect(self, val=True):
        if val:
            print("WARNING: WILL NOT INSPECT DLL, PHASE CANNOT BE GUARANTEED")
        self.not_inspect = val
        pass

    def upload_str(self):
        self.overwrite_gbtx2()
        out = ""
        for word in self.reg:
            out += word + "\n"
        return out


    def write_reg(self, reg, val):
        self.reg[reg] = val

    def read_phase(self):
        print("===> read phase from {0}".format(self.read_file_name))
        try:
            f = open(self.read_file_name)
        except IOError:
            exit("ERROR: you didn't run the automatic phase training yet. Please do it after roc is configured.")

        con_r = GBTXConfigHandler("read_file", f, self.flx_card, self.fiberNo, self.ICaddr)

        if len(con_r.reg) == 0:
            return self.read_file_name
        else:
            # set as manual mode for phase aligner:
            self.reg[62] = phase_mode["static"]

            # set phases
            for iregw, iregr in [
                    # group 0 channel 7-0
                    (66,  402),
                    (67,  401),
                    (68,  400),
                    (69,  399),
                    (70,  402),
                    (71,  401),
                    (72,  400),
                    (73,  399),
                    (74,  402),
                    (75,  401),
                    (76,  400),
                    (77,  399),

                    # group 1 channel 7-0
                    (90,  406),
                    (91,  405),
                    (92,  404),
                    (93,  403),
                    (94,  406),
                    (95,  405),
                    (96,  404),
                    (97,  403),
                    (98,  406),
                    (99,  405),
                    (100, 404),
                    (101, 403),

                    # group 2 channel 7-0
                    (114, 410),
                    (115, 409),
                    (116, 408),
                    (117, 407),
                    (118, 410),
                    (119, 409),
                    (120, 408),
                    (121, 407),
                    (122, 410),
                    (123, 409),
                    (124, 408),
                    (125, 407),

                    # group 3 channel 7-0
                    (138, 414),
                    (139, 413),
                    (140, 412),
                    (141, 411),
                    (142, 414),
                    (143, 413),
                    (144, 412),
                    (145, 411),
                    (146, 414),
                    (147, 413),
                    (148, 412),
                    (149, 411),

                    # group 4 channel 7-0
                    (162, 418),
                    (163, 417),
                    (164, 416),
                    (165, 415),
                    (166, 418),
                    (167, 417),
                    (168, 416),
                    (169, 415),
                    (170, 418),
                    (171, 417),
                    (172, 416),
                    (173, 415),

                    # EC channel
                    #  (233,  398),
                    #  (237,  398),
                    #  (241,  398),

                    ]:
                print(
                        "setting old reg{0} val={1}".format( 
                            iregw, self.reg[iregw]), 
                        " to readback reg{0} val={1}".format( 
                            iregr, con_r.reg[iregr])
                        )

                # naive read
                self.reg[iregw] = con_r.reg[iregr]
            return None
        pass

    def read_config(self, val=0):
        """
        read the current config to a file
        """
        try:
            f = open(self.read_file_name, "w")
        except IOError:
            exit("You should run it under a directory where you have write permissing!")

        if self.ICaddr == 1:
            if val == 0:
                timeout_run( ["fice", 
                    "-G", str(self.fiberNo), 
                    "-I", str(self.ICaddr), 
                    "-d", str(self.flx_card)], stdout=f)
            else:
                timeout_run( ["fice", 
                    "-G", str(self.fiberNo), 
                    "-I", str(self.ICaddr), 
                    "-d", str(self.flx_card)])
        if self.ICaddr == 2:
            # old way with IC
            # os.system("fice -G {0} -I {1} -d {2} {3}".format(self.fiberNo, self.ICaddr, self.flx_card, self.write_file_name))

            # need to use I2c
            # at least need to config it (through this 
            #   or by connecting fiber, which is not feasible in run-3 because lack of felix)
            timeout_run(["/afs/cern.ch/user/p/ptzanis/public/ScaSoftware/build/Demonstrators/GbtxConfiguration/gbtx_configuration",
                "--address",
                "simple-netio://direct/{0}".format(self.hostname),
                "-i", "1",
                "-d", str(self.flx_card),
                "-r"
                ])

        f.close()

    # totally just like a helper
    def upload_single(self, reg, val):
        timeout_run( ["fice", 
            "-G", str(self.fiberNo), 
            "-I", str(self.ICaddr), 
            "-d", str(self.flx_card),
            "-a", str(reg), str(val)
            ])

        #  os.system("fice -G {0} -I {1} -d {2} -a {3} {4}".format(
            #  self.fiberNo, self.ICaddr, self.flx_card,
            #  reg, val,
            #  ))
        pass

    def upload_config(self):
        """
        write to a file and upload the current config
        """
        try:
            f = open(self.write_file_name, "w")
        except IOError:
            exit("You should run it under a directory where you have write permissing!")
        f.write(  self.upload_str() )
        f.close()

        # upload!
        if self.ICaddr == 1:
            #  os.system("fice -G {0} -I {1} -d {2} {3}".format(self.fiberNo, self.ICaddr, self.flx_card, self.write_file_name))
            timeout_run( ["fice", 
                "-G", str(self.fiberNo), 
                "-I", str(self.ICaddr), 
                "-d", str(self.flx_card),
                str(self.write_file_name)
                ])
        time.sleep(1)
        # the first time, upload for GBTx-2 is always not working..
        # give it another try another time
        if self.ICaddr == 2:
            # old way with IC
            # os.system("fice -G {0} -I {1} -d {2} {3}".format(self.fiberNo, self.ICaddr, self.flx_card, self.write_file_name))

            # need to use I2c
            # at least need to config it (through this 
            #   or by connecting fiber, which is not feasible in run-3 because lack of felix)
            timeout_run(["/afs/cern.ch/user/p/ptzanis/public/ScaSoftware/build/Demonstrators/GbtxConfiguration/gbtx_configuration",
                "--address",
                "simple-netio://direct/{0}".format(self.hostname),
                "-i", "1",
                "-d", str(self.flx_card),
                "-w", str(self.write_file_name)
                ])

            #  os.system("/afs/cern.ch/user/p/ptzanis/public/ScaSoftware/build/Demonstrators/GbtxConfiguration/gbtx_configuration --address simple-netio://direct/{0} -i 1 -d {1} -w {2}".format(
                #  self.hostname,
                #  self.flx_card, 
                #  self.write_file_name))

            time.sleep(1)
            pass
        pass

    def overwrite_dll(self):
        # Charge-Pump current
        # according to gbtx manual 41, #
        # better set to bb 0b, not dd 0d
        # TODO: check if it's the case
        self.reg[64] = "bb"
        self.reg[65] = "0b"
        self.reg[88] = "bb"
        self.reg[89] = "0b"
        self.reg[112] = "bb"
        self.reg[113] = "0b"
        self.reg[136] = "bb"
        self.reg[137] = "0b"
        self.reg[160] = "bb"
        self.reg[161] = "0b"
        # group 5-6
        #  self.reg[184] = phase_mode["bb"],
        #  self.reg[185] = phase_mode["0b"],
        #  self.reg[208] = phase_mode["bb"],
        #  self.reg[209] = phase_mode["0b"],
        # EC
        #  self.reg[231] = phase_mode["bb"],
        #  self.reg[232] = phase_mode["0b"],
        pass

    def upload_dll_reset(self):
        """
        If the chip has been previously configured by either I2C, IC - channel or the fuses have been fused, the initialization state machine will take care of doing the DLL reset cycle after the chip is reset (see chapter 10).
        """
        for i in range(65, 162, 24):
            self.upload_single(i, "7" + self.reg[i][1])
            self.upload_single(i, "0" + self.reg[i][1])
        pass


    def pa_train(self, on=True):
        # TODO: do i need to train group 0 (sca)
        #  group0 = [ 78, 79, 80 ]
        group0 = [  ]
        group_other = [
                102, 103, 104,
                126, 127, 128,
                150, 151, 152,
                ]
        group4 = [
                174, 175, 176,
                ]
        #  group_EC = [ 245 ]
        group_EC = [  ]


        if self.do_one_by_one:
            # a bit deprecated.. don't use
            if on:
                self.reg[62] = phase_mode["training"]
                # do reset cycle, too
                # +6 is reset
                for ireg in group0: 
                    self.upload_single(ireg,   "07")
                for ireg in group0: 
                    self.upload_single(ireg+6, "07")
                for ireg in group0: 
                    self.upload_single(ireg+6, "00")

                for ireg in group_other:
                    self.upload_single(ireg  , "01")
                for ireg in group_other:
                    self.upload_single(ireg+6, "01")
                for ireg in group_other:
                    self.upload_single(ireg+6, "00")

                for ireg in group4:
                    self.upload_single(ireg  , "01")
                for ireg in group4:
                    self.upload_single(ireg+6, "01")
                for ireg in group4:
                    self.upload_single(ireg+6, "00")

                for ireg in group_EC:
                    self.upload_single(ireg  , "08")
                for ireg in group_EC:
                    self.upload_single(ireg+6, "08")
                for ireg in group_EC:
                    self.upload_single(ireg+6, "00")
            else:
                for ireg in group_other + group0:
                    self.upload_single(ireg, "00")
        else:
            if on:
                # do reset cycle, too
                # +6 is reset
                for ireg in group0: 
                    self.write_reg(ireg,   "07")
                for ireg in group_other:
                    #  self.write_reg(ireg  , "11")
                    self.write_reg(ireg  , "01")
                for ireg in group4:
                    #  self.write_reg(ireg  , "13")
                    self.write_reg(ireg  , "01")
                for ireg in group_EC:
                    self.write_reg(ireg  , "08")
                # TODO: test if this is necessary? (save time)
                # i.e. set to train, then set to reset
                # avoid simultaneous cmd to cause confusion
                #  self.upload_config()

                # TODO: try train only channel 0?
                for ireg in group0: 
                    self.write_reg(ireg+6, "07")
                for ireg in group_other:
                    #  self.write_reg(ireg+6, "11")
                    self.write_reg(ireg+6, "01")
                for ireg in group4:
                    #  self.write_reg(ireg+6, "13")
                    self.write_reg(ireg+6, "01")
                for ireg in group_EC:
                    self.write_reg(ireg+6, "08")
                self.upload_config()

                for ireg in group0: 
                    self.write_reg(ireg+6, "00")
                for ireg in group_other:
                    self.write_reg(ireg+6, "00")
                for ireg in group4:
                    self.write_reg(ireg+6, "00")
                for ireg in group_EC:
                    self.write_reg(ireg+6, "00")
                self.upload_config()
            else:
                for ireg in group_other + group0 + group4 + group_EC:
                    self.write_reg(ireg, "00")
                self.upload_config()
                
        pass

    def train_phases(self,):
        print("===> start training")
        self.pa_train()

        #  if not self.not_inspect:
            #  print("====> INSPECT after train on")
            #  # return true if locked, 
            #  # what to do if else?
            #  self.inspect_lock()
        # turn off..
        self.pa_train(False)

        if not self.not_inspect:
            # well, check again?
            print("====> INSPECT after train off")
            is_locked = self.inspect_lock()
            if is_locked:
                print("everything is locked")
            return is_locked
        else:
            return True
        pass

    def inspect_lock(self):
        locked = True
        print("inspecting flx-card {0}, fiber {1},  ICaddr {2}".format(self.flx_card, self.fiberNo, self.ICaddr) )
        for reg, mask in [

                # to check group 0-4
                # (390, 0x1f),
                # to check group 0-4 and EC
                # (390, 0x9f),
                # to check group 1-4
                (390, 0x1e),

                # (391, 0x07),
                (392, 0x01),
                (393, 0x01),
                (394, 0x01),
                (395, 0x01),
                # EC
                #  (398, 0x10),
                ]:
            out = ""
            p = subprocess.Popen( ["fice", "-G", str(self.fiberNo), "-I", str(self.ICaddr), "-d", str(self.flx_card), 
                    "-a", str(reg)],
                    stdout=subprocess.PIPE )
            time.sleep(0.5)

            found = False
            for line in iter(p.stdout.readline, b''):
                if b"Reply" in line:
                    found = True
                elif found:
                    out = line.rstrip().split(b":")[1]
                    break

            #  print out
            try:
                val = int(out, 16)
            except:
                print("ERROR: something wrong with this link")
                return False

            if (val & mask) != mask:
                series = "{0:#07b}".format(mask - (val & mask))[:1:-1]
                print(val, series)
                for i in range(len(series)):
                    if series[i] == "0":
                        continue
                    locked = False
                    if reg == 390:
                        print("Group {0} not locked. Group 7 means EC".format(i))
                    elif reg == 398:
                        print("EC channel not locked:")
                    else:
                        print("Group {0} channel {1}"" not locked".format(reg - 391, i))

        return locked
