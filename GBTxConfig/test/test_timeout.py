#!/usr/bin/env python3
import subprocess
import time

def timeout_run(*arg, **kwarg):
    try:
        subprocess.run(*arg, **kwarg)
    except TimeoutExpired:
        print("WARNING! Timeout the process!")

timeout_run(["ping", "localhost"], timeout=3)
#  timeout(subprocess.call("top") , 10)

#  print task.poll()

#  t = 1
#  delay = 1

#  while task.poll() is None and t > 0:
     #  # do other things too if necessary e.g. print, check resources, etc.
     #  time.sleep(delay)
     #  t -= delay
