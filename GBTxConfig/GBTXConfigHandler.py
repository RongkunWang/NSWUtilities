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

import os, time, math
import subprocess

def green(*l):
    return ansi_color(32, *l)

def red(*l):
    return ansi_color(31, *l)

def ansi_color(color, *l):
    out = "\033[{0}m".format(color)
    for a in l:
        out += str(a) + " " 
    out += "\033[0m"
    return out

dict_rate = {
        0:  "00",
        80: "15",
        160:"2a",
        320:"3f", 
        }

# backward compatible..
dict_phase = dict_rate

# phase aligner mode
phase_mode = {
    "static":"00",
    "training":"15",
    "tracking":"2a",
    "none":"3f",
}

def timeout_run(*arg, **kwargs):
    try:
        print("going to run: {0}".format(" ".join(arg[0])))
    except e:
        print("WARNING: this command is a bit weird.")

    try:
        # fine tuning
        return subprocess.run(*arg, **kwargs, timeout = 3)
    except subprocess.TimeoutExpired:
        print("WARNING! Timeout the process! Shouldn't affect uploaded values")
    except e:
        print("unexpected exception", sys.exc_info()[0])

class GBTXConfigHandler():
    def __init__(self, tp, val, _flx_card, _fiberNo, _ICaddr, hostname="", dir="GBTXconfigs"):
        """
        tp can be: 
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
        self.turn_off = True

        if os.environ["HOSTNAME"] in [
                "um-felix1", 
                "um-felix1.cern.ch", 
                "um-felix2", 
                "um-felix2.cern.ch",
                ]:
            #  print(os.environ["HOSTNAME"])
            self.gbtx_exe = "/afs/cern.ch/user/p/ptzanis/public/ScaSoftware/build/Demonstrators/GbtxConfiguration/gbtx_configuration"
        else:
            self.gbtx_exe = "/afs/cern.ch/work/n/nswdaq/public/ScaSoftware/installed/bin/gbtx_configuration"
        self.gbtx_exe_kwargs = {}

        self.channel_bit = {
                0:"07",
                1:"01",
                2:"01",
                3:"01",
                4:"01",
                }
        self.mask_group = [
                # (391, 0x07),
                (392, 0x01),
                (393, 0x01),
                (394, 0x01),
                (395, 0x01),
                # EC
                #  (398, 0x10),
                ]

        os.system("mkdir -p {0}".format(dir))

        self.write_file_name = "{3}/upload_card{0}_link{1}_gbt{2}.txt".format(
                _flx_card, _fiberNo, _ICaddr, dir)
        self.read_file_name  = "{3}/read_card{0}_link{1}_gbt{2}.txt".format(
                _flx_card, _fiberNo, _ICaddr, dir)
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

    def do_not_turn_off(self):
        self.turn_off = False

    def setI2CExe(self, in_exe, **kwargs):
        self.gbtx_exe = in_exe
        self.gbtx_exe_kwargs = kwargs

    def set_MM(self):
        self.channel_bit = {
                0:"ff",
                1:"ff",
                2:"ff",
                3:"ff",
                4:"ff",
                }
        # TODO: confirm this check work
        self.mask_group = [
                # (391, 0x07),
                (392, 0x75),
                (393, 0x11),
                (394, 0x11),
                (395, 0x11),
                # EC
                #  (398, 0x10),
                ]

    def set_sTGC_640(self):
        self.channel_bit = {
                0:"07",
                1:"11",
                2:"11",
                3:"11",
                4:"11",
                }
        self.mask_group = [
                # (391, 0x07),
                (392, 0x11),
                (393, 0x11),
                (394, 0x11),
                (395, 0x11),
                # EC
                #  (398, 0x10),
                ]

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

    def get_reg(self, reg):
        return self.reg[reg]

    def upload_single_phase(self, gr, ch, val):
        """
        read from felix into a file then into memory, then modify the phase manually
        input: int, int, str
        """
        self.read_config()
        self.read_phase()
        #  self.upload_single( 62, phase_mode["static"] )
        for arg in self.set_phase(gr, ch, val):
            print(arg)
            #  self.upload_single( *arg )

    def set_phase(self, gr, ch, val):
        """
        input: int, int, str
        """

        # val is form of single-byte two-hex words
        ch_base = 66 + gr * 24
        for this_reg in [
                ch_base + (3 - math.floor(ch / 2)),
                ch_base + (3 - math.floor(ch / 2)) + 4,
                ch_base + (3 - math.floor(ch / 2)) + 8,
                ]:
            new = self.reg[this_reg]
            #  print(this_reg, new, new[1])
            index = ch % 2
            if index == 0:
                self.reg[this_reg] = new[0] + val
            else:
                self.reg[this_reg] = val + new[1]
            #  print(self.reg[this_reg])
            yield (this_reg, self.reg[this_reg])
            pass
        pass
        #  self.reg[]

    def read_file(self):
        """
        read all the config from a file and generate a handler
        """
        print("===> read phase from {0}".format(self.read_file_name))
        try:
            f = open(self.read_file_name)
        except IOError:
            exit("ERROR: you didn't run the automatic phase training yet. Please do it after roc is configured.")

        con_r = GBTXConfigHandler("read_file", f, self.flx_card, self.fiberNo, self.ICaddr)
        f.close()
        print(con_r.reg)
        return con_r

        pass

    def print_phase(self):
        self.read_config()
        con_r = self.read_file()
        if len(con_r.reg) == 0:
            print("nothing in the registers")
            return
        for group in range(1, 5):
            print("channel 7-0, group {0}".format(group))
            for iregr in range(402, 398, -1):
                print("Phases are {0}".format(con_r.reg[iregr + group * 4]))
                pass
            print()
            pass
        pass


    def read_phase(self):
        """
        read from the readback file and set the registers to current phase
        """
        con_r = self.read_file()
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
        read the current config from FELIX to a file
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
            timeout_run([self.gbtx_exe, 
                "--address",
                "simple-netio://direct/{0}".format(self.hostname),
                "-i", "1",
                "-d", str(self.flx_card),
                "-r"
                ], **self.gbtx_exe_kwargs)

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
            timeout_run([self.gbtx_exe,
                "--address",
                "simple-netio://direct/{0}".format(self.hostname),
                "-i", "1",
                "-d", str(self.flx_card),
                "-w", str(self.write_file_name)
                ], **self.gbtx_exe_kwargs)

            time.sleep(1)
            pass
        pass

    def overwrite_dll(self):
        # Charge-Pump current
        # according to gbtx manual 41, #
        # better set to bb 0b, not dd 0d
        # TODO: check if it's the case
        #  self.reg[64] = "bb"
        #  self.reg[65] = "0b"



        for i in [88,
                112,
                136,
                160,
                ]:
            self.reg[ i ] = "bb"
            self.reg[i+i] = "0b"

            #  self.upload_single(i, "bb")
            #  self.upload_single(i+1, "0b")

            #  self.upload_single(i+1, "7d")
            #  self.upload_single(i+1, "0d")
        #  self.upload_config()

        #  self.reg[88] = "bb"
        #  self.reg[89] = "0b"

        #  self.reg[112] = "bb"
        #  self.reg[113] = "0b"

        #  self.reg[136] = "bb"
        #  self.reg[137] = "0b"

        #  self.reg[160] = "bb"
        #  self.reg[161] = "0b"
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
        # do not do for group 0 (sca)
        #  group0 = [ 78, 79, 80 ]
        groups = [1, 2, 3, 4]
        group_base = [78, 79, 80]
        #  group_other = [
                #  102, 103, 104,
                #  126, 127, 128,
                #  150, 151, 152,
                #  174, 175, 176,
                #  ]
        # do not do for EC (sca)
        #  group_EC = [ 245 ]
        group_EC = [  ]

        if self.do_one_by_one and self.ICaddr != 2:
            # a bit deprecated.. don't use
            if on:
                # do reset cycle, too
                # +6 is reset
                # DEBUG send like this?
                self.upload_single(62, phase_mode["training"])
                for egrp in groups:
                    for base in group_base:
                        self.upload_single(base + 24 * egrp, self.channel_bit[egrp])
                    for base in group_base:
                        self.upload_single(base + 24 * egrp + 6, self.channel_bit[egrp])
                    for base in group_base:
                        self.upload_single(base + 24 * egrp + 6, "00")
                    if self.turn_off:
                        for base in group_base:
                            self.upload_single(base + 24 * egrp, "00")
                            pass

                for ireg in group_EC:
                    self.upload_single(ireg  , "08")
                for ireg in group_EC:
                    self.upload_single(ireg+6, "08")
                for ireg in group_EC:
                    self.upload_single(ireg+6, "00")
            else:
                pass
                #  for base in group_base:
                    #  for egrp in groups:
                        #  self.upload_single(base + 24 * egrp, "00")
        else:
            self.write_reg(62, phase_mode["training"])
            if on:
                # do reset cycle, too
                # +6 is reset
                for base in group_base:
                    for egrp in groups:
                        self.write_reg(base + 24 * egrp, self.channel_bit[egrp])
                for ireg in group_EC:
                    self.write_reg(ireg  , "08")
                # TODO: test if this is necessary? (save time)
                # i.e. set to train, then set to reset
                # avoid simultaneous cmd to cause confusion
                #  self.upload_config()

                # TODO: try train only channel 0?
                for base in group_base:
                    for egrp in groups:
                        self.write_reg(base + 24 * egrp + 6, self.channel_bit[egrp])
                for ireg in group_EC:
                    self.write_reg(ireg+6, "08")
                self.upload_config()

                for base in group_base:
                    for egrp in groups:
                        self.write_reg(base + 24 * egrp + 6, "00")
                for ireg in group_EC:
                    self.write_reg(ireg+6, "00")
                self.upload_config()
            else:
                for base in group_base:
                    for egrp in groups:
                        self.write_reg(base + 24 * egrp, "00")
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
        if self.turn_off:
            self.pa_train(False)

        if not self.not_inspect:
            # well, check again?
            print("====> INSPECT after train off")
            is_locked = self.inspect_lock()
            if is_locked:
                print(green("everything is locked"))
            return is_locked
        else:
            return True
        pass

    def inspect_lock(self):
        locked = True
        print("inspecting flx-card {0}, fiber {1},  ICaddr {2}".format(self.flx_card, self.fiberNo, self.ICaddr) )
        to_check = [

                # to check group 0-4
                # (390, 0x1f),
                # to check group 0-4 and EC
                # (390, 0x9f),
                (390, 0x1e),
                # to check group 1-4
                ] + self.mask_group
        for reg, mask in to_check:

            out = ""
            # TODO: see if this works
            p = timeout_run(["fice",
                "-G", str(self.fiberNo),
                "-I", str(self.ICaddr),
                "-d", str(self.flx_card),
                "-a", str(reg)],
                stdout=subprocess.PIPE )
            #  p = subprocess.Popen( ["fice", "-G", str(self.fiberNo), "-I", str(self.ICaddr), "-d", str(self.flx_card), 
                    #  "-a", str(reg)],
                    #  stdout=subprocess.PIPE )
            time.sleep(0.5)

            found = False
            if p:
                for line in p.stdout.split(b'\n'):
                    if b"Reply" in line:
                        found = True
                    elif found:
                        out = line.rstrip().split(b":")[1]
                        break

            #  print out
            try:
                val = int(out, 16)
            except:
                print(red("ERROR: something wrong with this link data: {0}".format(out)))
                return False

            if (val & mask) != mask:
                channel_check = "{0:08b}".format(mask)
                #  series = "{0:08b}".format(mask - (val & mask))[::-1]
                #  print(series)
                # reverse
                series = "{0:08b}".format(val & mask)[::-1]
                print(reg, channel_check)
                print(reg, val, series)
                for i in range(len(series)):
                    if channel_check[i] == "0": continue
                    if series[i] == "1": continue
                    locked = False
                    if reg == 390:
                        print(red("Group {0} not locked. Group 7 means EC".format(i)))
                    elif reg == 398:
                        print(red("EC channel not locked:"))
                    else:
                        print(red("Group {0} channel {1}"" not locked".format(reg - 391, 7 - i)))

        return locked
