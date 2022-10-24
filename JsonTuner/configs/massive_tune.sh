#!/bin/bash
for side in A C; do
    for sec in {01..16}; do
        word=$side$sec
        echo $word
        cat ${word}.py | awk -v d=4 '/ROFFSET[[:space:]]*=/{$3-=d}1' | \
            awk -v d=4 '/LOFFSET[[:space:]]*=/{$3-=d}1' | \
            awk -v d=4 '/TPOFFSET[[:space:]]*=/{$3-=d}1' > ${word}_DownShift4.py
    done
done
