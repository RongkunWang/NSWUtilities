#!/bin/bash
echo "Sector,ROffset,LOffset,TPOffset" > summary.csv
for side in A C; do
    for sec in {01..16}; do
        word=$side$sec
        v1=$(grep ROFFSET ${word}.py  | grep -v "cfg_bcid0\|gloSyncBcidOffset\|!=" | tr -s ' ' | cut -f 3 -d" ")
        v2=$(grep LOFFSET ${word}.py  | grep -v "cfg_bcid0\|gloSyncBcidOffset\|!=" | tr -s ' ' | cut -f 3 -d" ")
        v3=$(grep TPOFFSET ${word}.py | grep -v "cfg_bcid0\|gloSyncBcidOffset\|!=" | tr -s ' ' | cut -f 3 -d" ")
        echo "$word,$v1,$v2,$v3" >> summary.csv
    done
done
