#!/usr/bin/env python3
import glob, os
from pathlib import Path

#  input
for i in glob.glob("/eos/user/r/rowang/work/NSW/official-json-configs/mmg/readout/*json"):
    print(Path(i).name, i)

    #  os.system(f"./tuneOfficialJson.py -i {i} -o official-json-configs/mmg/readout/{Path(i).name} -s             {Path(i).name[:3]}_auto")
    #  os.system(f"./tuneOfficialJson.py -i {i} -o official-json-configs/mmg/readout/{Path(i).name} -s MMG_Trigger")
    #  os.system(f"./tuneOfficialJson.py -i {i} -o official-json-configs/mmg/readout/{Path(i).name} -s MMG_Trigger,{Path(i).name[:3]}_auto")
    #  os.system(f"./addTPCarrier.py -i {i} -o official-json-configs/mmg/readout/{Path(i).name}")
    os.system(f"./upgrade_mmtp_json.py {i} official-json-configs/mmg/readout/{Path(i).name}")
    #  break # for testing
    pass

#  for i in glob.glob("/eos/user/r/rowang/work/NSW/official-json-configs/stgc/readout/*json"):
    #  print(Path(i).name)
    #  os.system(f"./addTPCarrier.py -i {i} -o official-json-configs/stgc/readout/{Path(i).name}")
    #  os.system(f"./tuneOfficialJson.py -i {i} -o official-json-configs/stgc/readout/{Path(i).name} -s MMG_Trigger")
    #  pass
