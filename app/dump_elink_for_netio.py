#!/usr/bin/env python3
import ElinkDict

def shift_flxid(i, id = 0):
    return i + id * 2**16

#  FLXID = 6
#  FLXID = 12
FLXID = 8

#  dic = ElinkDict.MMElinkDict_191_A16
#  dic = ElinkDict.MMElinkDict_191
dic = ElinkDict.sTGCElinkDict

for i in dic.keys():
    if i < 2048:
        print (shift_flxid(i, FLXID), end=" ")
print()
print()


for i in dic.keys():
    if i > 2048 and i < 2048 * 2:
        print (shift_flxid(i, FLXID), end=" ")
print()
print()

for i in dic.keys():
    if i > 2048 * 2 and i < 2048 * 3:
        print (shift_flxid(i, FLXID), end=" ")
print()
print()

for i in dic.keys():
    if i > 2048 * 3 and i < 2048 * 4:
        print (shift_flxid(i, FLXID), end=" ")
print()
print()

