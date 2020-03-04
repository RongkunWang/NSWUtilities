#!/bin/bash

rawdata=$1
data=`echo $1 | rev | cut -d. -f2- | rev`_simple.root
# data_test.1580224485._2sFEB0p27.daq.RAW._lb0000._NSW_SWROD._0001.data
nsw_process --rootsimple -i  $rawdata
./hit_RDF.py $data
root -l $data
