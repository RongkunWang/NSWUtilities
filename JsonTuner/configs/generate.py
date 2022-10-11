#!/usr/bin/env python
import os


for i in range(1, 17):
    sector = f"{i:02d}"
    os.system(f"cp A01.py C{sector}.py")
    if i in [1, 9]: continue
    os.system(f"cp A01.py A{sector}.py")
