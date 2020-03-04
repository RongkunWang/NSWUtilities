#!/bin/bash

# cd /afs/cern.ch/user/n/nswdaq/public/sw/external/nswdaq/x86_64-centos7-gcc8-opt
# source setup.sh
# cd -

# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/afs/cern.ch/user/n/nswdaq/public/sw/external/nswdaq/installed/x86_64-centos7-gcc8-opt/lib
# alias nsw_process=/afs/cern.ch/user/n/nswdaq/public/sw/external/nswdaq/installed/x86_64-centos7-gcc8-opt/bin/nsw_process


# this version has fixed the duplicate event bug
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/afs/cern.ch/work/r/rowang/public/FELIX/nsw_daq/installed/x86_64-centos7-gcc8-opt/lib
# source /cvmfs/sft.cern.ch/lcg/releases/LCG_95/ROOT/6.16.00/x86_64-centos7-gcc8-opt/bin/thisroot.sh
# alias nsw_process=/afs/cern.ch/work/r/rowang/public/FELIX/nsw_daq/installed/x86_64-centos7-gcc8-opt/bin/nsw_process


# source /afs/cern.ch/atlas/project/tdaq/cmake/cmake_tdaq/bin/cm_setup.sh tdaq-08-02-00
source /afs/cern.ch/user/n/nswdaq/public/proc/setup.sh
source /afs/cern.ch/user/n/nswdaq/public/proc/installed/setup.sh
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/afs/cern.ch/user/n/nswdaq/public/proc/installed/x86_64-centos7-gcc8-opt/lib
# source /cvmfs/sft.cern.ch/lcg/views/LCG_95/x86_64-centos7-gcc8-opt/setup.sh
# source /cvmfs/sft.cern.ch/lcg/releases/LCG_95/ROOT/6.16.00/x86_64-centos7-gcc8-opt/bin/thisroot.sh
alias nsw_process="/afs/cern.ch/user/n/nswdaq/public/proc/installed/x86_64-centos7-gcc8-opt/bin/nsw_process --rootsimple -i "
# export PATH="/afs/cern.ch/user/p/patmasid/public/Felix_Analysis:$PATH"

# function quickAnalHit { 
  # the_dir="/afs/cern.ch/user/p/patmasid/public/felixdata_minitreeanalysis/"
  # tag=`echo $1 | rev | cut -d'_' -f 2- | rev`
  # $the_dir/analHit $1 $the_dir/src/ElinkFebFiberMapping/ElinkFebFiberMapping_v1.txt ${tag}_decoded.root
# }
# export -f quickAnalHit
