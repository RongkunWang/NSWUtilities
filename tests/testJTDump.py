#!/usr/bin/env python

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import JsonTuner.tests.test_module as tm

if __name__ == "__main__":
    print("This is a test module for dump")
    tm.test_dump()
