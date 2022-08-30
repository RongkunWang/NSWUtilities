#!/usr/bin/env python3
import glob, os
from pathlib import Path

#  ./tuneOfficialJson.py -i /eos/home-r/rowang/work/NSW/official-json-configs/mmg/readout/C09_thrRMSx15_Masked.json -o test.json -s MMG_Trigger
for i in glob.glob("/eos/home-r/rowang/work/NSW/official-json-configs/mmg/readout/*"):
    print(Path(i).name)
    os.system(f"./tuneOfficialJson.py -i {i} -o official-json-configs/mmg/readout/{Path(i).name} -s MMG_Trigger")

