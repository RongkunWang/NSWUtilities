#! /usr/bin/env tdaq_python

import os, shutil, pathlib, argparse
import collections
import pm.project
from config.dal import module as dal_module
from pm.dal import dal

parser = argparse.ArgumentParser(description = "Quick way to disable/enable things in oks")
parser.add_argument('-E', dest = "enableSet", default = [],
        nargs = "+", help = "enable  elements")
parser.add_argument('-N', dest = "disableSet", default = [],
        nargs = "+", help = "disable elements")
parser.add_argument("-p", dest = "part", default = "ATLAS", type = str, help = "the partition to run")
parser.add_argument("-m", dest = "msg",  required = True, type = str, help = "the commit message to use")
args = parser.parse_args()


predefinedSet = { }

for side in ["A", "C"]:
    for sector in range(1, 17):
        for tech in ["MMG", "STG"]:
            predefinedSet["{}{}{:02d}".format(tech, side, sector)] = [
                    "{}-{}-S{:02d}-swRodModule".format(tech, side, sector),
                    "NSW-{}-E{}-S{:02d}-Noise-ConfigApplication".format(tech, side, sector),
                    ]
            pass
        pass
        predefinedSet["MMTP{}{:02d}".format(side, sector)] = [
                "MMG-{0}{1:02d}_MMTP_{0}{1:02d}".format(side, sector),
                "MMG-{}{:02d}_ADDCs".format(side, sector),
                    ]
        predefinedSet["NSW{}{:02d}".format(side, sector)] = \
                predefinedSet["MMG{}{:02d}".format(side, sector)] + \
                predefinedSet["STG{}{:02d}".format(side, sector)] + \
                predefinedSet["MMTP{}{:02d}".format(side, sector)] + [
                    "NSW-{}-S{:02d}-swRod".format(side, sector),
                    "NSW-{}-S{:02d}-Gnam".format(side, sector),
                    ]
    pass

partitionFileDict = {
        "ATLAS": "combined/partitions/ATLAS.data.xml",
        }
for i in [
    "part_MMG_A_Noise",
    "part_MMG_C_Noise",
    "part_STG_A_Noise",
    "part_STG_C_Noise",
    "part_MMG_A_Calib",
    "part_MMG_C_Calib",
    "part_STG_A_Calib",
    "part_STG_C_Calib",
    ]: 
    partitionFileDict[i] = "muons/partitions/{}.data.xml".format(i)
        
partitionNameDict = {
        "atlas": "ATLAS",
        "atlas": "ATLAS",
        }


################
# preparation
################
USER = os.environ["USER"]
oksDir = pathlib.Path("/tmp/{}-oks".format(USER))
os.environ["TDAQ_DB_USER_REPOSITORY"] = str(oksDir)
os.environ["TDAQ_DB_PATH"] = str(oksDir)
shutil.rmtree(oksDir, ignore_errors = True)
oksDir.mkdir()
os.system("oks-checkout.sh")

partFile = pm.project.Project(partitionFileDict[args.part])
part = partFile.getObject("Partition", args.part)

# if both enable and disable, enable first
sDisable = set()
sEnable  = set()
objToProcess = collections.deque(part.Segments) 
while len(objToProcess) != 0:
    seg = objToProcess.popleft()
    if seg.__class__.__name__ == "Segment": 
        for i in seg.Segments:
            objToProcess.append(i)
        for i in seg.Resources:
            objToProcess.append(i)
    if len(set(["ROS", "ResourceSetAND", "ResourceSet", "ResourceSetOR"]).intersection(set([i.__name__ for i in seg.__class__.__bases__])) ) != 0:
        for i in seg.Contains:
            objToProcess.append(i)

    for s in args.disableSet:
        if s not in predefinedSet:
            if s in seg.id:
                sDisable.add( seg )
            continue
        for objId in predefinedSet[s]:
            if objId in seg.id:
                sDisable.add( seg )
                pass
            pass
        pass
    for s in args.enableSet:
        if s not in predefinedSet:
            if s in seg.id:
                sEnable.add( seg )
            continue
        for objId in predefinedSet[s]:
            if objId in seg.id:
                sEnable.add( seg )
                pass
            pass
        pass
    pass


# do not enable the one we need to disable later
sEnable -= sDisable

print("##########################################")
# enable first
for seg in sEnable:
    if seg in part.Disabled:
        print("ENABLING", seg.fullName())
        part.Disabled.remove(seg)
    else:
        print("keep ", seg.fullName(), "ENABLED")
    pass
# then disable
print()
for seg in sDisable:
    if seg not in part.Disabled:
        print("DISABLING", seg.fullName())
        part.Disabled.append(seg)
    else:
        print("keep ", seg.fullName(), "DISABLED")
    pass
print("##########################################")

partFile.update_dal(part)
partFile.commit(args.msg)
print("Please review your changes and do:\n oks-commit.sh -u {} -m \"{}\"".format(oksDir, args.msg))
