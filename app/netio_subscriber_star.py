#! /usr/bin/env python3
"""
netio_subscriber.py - a script to subscribe and log netio_cats for various elinks

Run like:
    netio_subscriber.py -t 0x700ea 0x700ea 0x700ea
or
    netio_subscriber.py -d <elink-grp1>,<flx-id-1> <elink-grp2>,<flx-id-2>

The first way can be called together with the second way. But at least one of
them is needed. The port number is smartly handled by rules on the elink
numbers, it's not recommended to use -p to pass in a single port, as you would
possibly subscribe to multiple port.

In the first way of calling, the hostname must contain a "felix" string. 
It will use localhost as default, and if it's not proper hostname, you will 
have to specify the hostname with `-host`.

The second way of calling will look up <elink-grp> in the ELinkDict.py,
specified in -lib-path argument, and subscribe the corresponding elinks to 
the given pcatlnswfelix<id>. The elinks defined in the ELinkDicts will 
be `& 0xffff` so if your device is on felix07, you only need to put 
id=7, no need to think of other offsets inside the ELinkDict. 

In Both ways, you can exit by Ctrl+C the SIGINT.

By default, the program will create a directory with unique timetag, and one
file for each elink inside the directory. The file will be written in realtime
and is managed by subprocess.Popen(). If --nosave is given, the program will
print all subscribed elinks on the screen. 

Further information:
The e-link ID is an X-bit number
bits [X:16] encode the felix ID
bits [15:14] are 0 (my assumption from rongkun's comments)
bits [13:12] encode the felix device (assuming there are at most 4 devices that can be encoded per FELIX)
bits [11:0] encode the base e-link ID
"""
# remove the dependency on felix py environ before argparse
 
import sys
indexes = []
for i, lib in enumerate(sys.path):
    if "/opt/felix" in lib: indexes.append(i)
for i in sorted(indexes, reverse=True):
    del sys.path[i]

import os

import xml.etree.ElementTree as ET
import argparse
import socket
from datetime import datetime
import subprocess
import time
import signal
import pathlib


def options():
    """ argument parser to handle inputs from the user """
    parser = argparse.ArgumentParser(
        usage=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    #  arg_elink_group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "-s",
        dest="simulation",
        help="Simulation mode, do not subscribe.",
        action="store_true",
    )
    parser.add_argument(
            "-D",
            dest="directory",
            default = "/atlas/oks/tdaq-09-04-00/muons/segments/NSW/ELinks",
            type=str,
            help="directory to scan to get the list of elinks")
    parser.add_argument(
        "-t",
        help="The elinks to be subscribed to. Could be given in hex or decimal.",
        default="",
        nargs="+",
    )
    parser.add_argument(
        "-d",
        dest="elink_dict",
        help="The elinks dictionary we need to subscribe to <elink_grp>,<flx-id> \n" 
        "Please use raw names in ELinkDict, run with -d 1,1 in order to get help message",
        type=str,
        default=None,
        nargs="+",
    )
    parser.add_argument(
        "-lib-path",
        dest="lib_path",
        help="the directory containing elink_dict",
        default="/afs/cern.ch/user/n/nswdaq/workspace/public/nswdaq/current/nswdaq/installed/share/bin/"
        )
    parser.add_argument(
        "-offset",
        help="The Felix ID offset the user would like to merge with inputted local-to-the-felix e-link IDs (in range 0 -8191).",
        default=0,
        type=int,
    )
    parser.add_argument(
        "-e",
        help="Encoding for the data part of messages. Check netio_cat --help for more info.",
        default="raw",
    )
    parser.add_argument(
        "-o", help="Name of the output directory for your log files.", default=""
    )
    parser.add_argument(
        "--nosave",
        help="Only output the netio_cat to screen. Do not save to log files.",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        help="The felix port that you would like to subscribe to (ex. for BB5 12350/12351).",
        default="",
    )
    parser.add_argument(
        "-host",
        help="The FELIX host. For users that are not on a FELIX machine, e.g. from the swrod.",
        default="",
    )
    parser.add_argument(
        "--dir",
        help="The output directory.",
        default="/tmp",
    )
    return parser.parse_args()



def parse_elinks(elinks, offset):
    """if the elinks are given in hex as indicated by a 0x in the first element then return the list as is.
    If they are given in decimal then convert to hex. If an offset is given then add the offset."""
    if offset:
        rawelinks = [
            0xffff & int(elink, 16) if "0x" in elink else 0xffff & int(elink)
            for elink in elinks
        ]
        return [(offset << 16) + elink for elink in rawelinks]
    return [int(elink, 16) if "0x" in elink else int(elink, 10) for elink in elinks]


def fatal(msg):
    sys.exit(f"Fatal error: {msg}")


def felixhost(host):
    """ Get the felix host name from the socket. If a host is given override this. Check that the hostname is a valid felix host """
    hostname = socket.gethostname().rstrip(".cern.ch")
    if host:
        hostname = host
    if "felix" not in hostname.lower() and "flx" not in hostname.lower():
        fatal(
            f"The hostname {hostname} is not a valid FELIX host. Please supply one with the flag -host."
        )
    return hostname



def GetElinks(ifile):
    """
    takes a 
    """
    out = []
    l_elinks = []
    l_detName = []
    tree = ET.parse(ifile)
    root = tree.getroot()
    elink = "0"
    det_name = "0"
    for child in root: 
        if child.tag != "obj": continue
        if "SwRodInputLink" != child.attrib['class']: continue
        if "L1A" not in child.attrib['id']: continue
        for attr in child:
            if attr.attrib['name'].lower() == "felixid":
                elink = attr.attrib['val']
            if attr.attrib['name'].lower() == "detectorresourcename":
                det_name = attr.attrib['val']
                #  break
        #  l_elinks.append( int(elink, 16) )
        l_elinks.append( elink )
        l_detName.append( det_name )
    print(l_elinks, l_detName)


    # decimal
    #  d_host = {}

    # dict
    #  cmd = subprocess.Popen(["felix-buslist", "-e", "-i", "vlan413"], 
            #  stdout=subprocess.PIPE)
    #  iteration = 0

    #  while True:
        #  output = cmd.stdout.readline()
        #  if cmd.poll() is not None: break
        #  if not output: continue

        #  output = output.strip().decode("utf-8")
        #  if len(output) == 0: continue
        #  if output.startswith("Update"): continue
        #  if output.startswith("Elink"): continue
        #  if output.startswith("Tables"): continue
        #  l = output.split()
        #  dec_elink = int(l[0])
        #  d_host[ dec_elink ] = l[1].split(":")[1][len("//"):]

        #  iteration += 1

        #  if iteration % 10000 != 0:
            #  continue

        #  all_in = True
        #  for elink in l_elinks:
            #  if elink not in d_host:
                #  all_in = False
                #  break
            #  pass
        #  if all_in:
            #  print("all in")
            #  break
        #  pass
    #  for elink in l_elinks:
        #  out.append( (d_host[elink], elink ) )
    return l_elinks, l_detName

def main():
    # check user args
    ops = options()

    l_det = []

    # grab the options of netio_cat
    elinks = []
    hostnames = []
    pathlib.Path(f"{ops.dir}").mkdir(parents=True, exist_ok=True)
    outdir = ops.o if ops.o else f"{ops.dir}/netio_cat_elink_logs"
    if not (ops.elink_dict or ops.t):
        sys.exit('No action requested, add -t or -d')
    if ops.elink_dict: 
        dic_grps = {}
        for fname in os.listdir(ops.directory):
            if fname in [
                    "NSW-Elinks.data.xml",
                    "NSW-Elinks-MM-A.data.xml",
                    "NSW-Elinks-MM-C.data.xml",
                    "NSW-Elinks-MM.data.xml",
                    "NSW-Elinks-sTGC-A.data.xml",
                    "NSW-Elinks-sTGC-C.data.xml",
                    "NSW-Elinks-sTGC.data.xml",
                    ]: continue
            dic_grps[fname.split('.')[0][11:]] = os.path.join(ops.directory, fname)
            pass
        print(len(dic_grps))
        # the key are the one before the dots, after the Elinks-
        for elink_grp in ops.elink_dict:
            #  try:
                #  elink_grp, flxid = args.split(",")
            #  except ValueError as e:
                #  print(e)
                #  sys.exit("for -d, please specify <elink-grp>,<flx-id> ")
            #  flxid = int(flxid, 10)
            if elink_grp not in dic_grps:
                raise Exception(f'"{elink_grp}" does not exist in: {list(dic_grps.keys())}')
            outdir += f"_{elink_grp}"

            # TODO: change here to read!
            #  for host, elink in GetElinks(dic_grps[elink_grp]):
                #  hostnames.append(host)
                #  elinks.append(elink)
            elinks, l_det = GetElinks(dic_grps[elink_grp])
            print(elinks, l_det)
        pass
    
    l_det += ["dummy" for i in ops.t]
    elinks += ops.t
    #  elinks += parse_elinks(ops.t, ops.offset)
    #  hostname = felixhost(ops.host)
    #  hostnames += [hostname for i in elinks]
    #  encoding = ops.e

    # make the output dir
    now = datetime.now().strftime("%Y_%m_%d_%Hh%Mm%Ss")
    outdir += f"_{now}"
    os.mkdir(outdir)

    #  print(elinks)

    jobs = []
    l_output = []
    for det, elink in zip( l_det, elinks):  # decimal,
        tag = det.replace("/", "_")
        path = os.path.join(outdir, f"Det.{tag}.Fid.{elink}.log")
        netio = (f"felix-test-swrod --bus-dir=/detwork/nsw/felix/bus --fid {elink} --dump vlan413")
        print(netio)
        netio = netio.split()
        print(netio)

        if ops.simulation:
            continue

        def preexec_function():
            signal.signal(signal.SIGINT,  signal.SIG_IGN)
            signal.signal(signal.SIGTSTP, signal.SIG_IGN)
            signal.signal(signal.SIGQUIT, signal.SIG_IGN)
            pass
        if not ops.nosave:
            l_output.append(open(path, "w"))
            jobs.append(subprocess.Popen(netio, stdout=l_output[-1],    preexec_fn=preexec_function, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True))
        else:
            jobs.append(subprocess.Popen(netio, stderr=subprocess.STDOUT, preexec_fn=preexec_function))

    def sigquit_handler(signal_received, frame):
        print("received Ctrl+\, can't exit gracefully, ignoring. Please use Ctrl+C")
        pass
    signal.signal(signal.SIGQUIT, sigquit_handler)

    def sigtstp_handler(signal_received, frame):
        print("""received Ctrl+Z, main function suspending, please use 
        killall -9 felix-test-swrod 
        after you finish the test""")
        exit()
        pass

    signal.signal(signal.SIGTSTP, sigtstp_handler)
    print("Press Ctrl+C to finish data taking...")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        print("received Ctrl+C, stop data taking"+\
                "")

    for job in jobs:
        job.terminate()
    for of in l_output:
        of.close()
    print("Done cleaning up.")

if __name__ == "__main__":
    main()
