# for i in {0..11}; do
    # printf -v s "%02d" $i
    # ssh pc-tdq-flx-nsw-mm-$s "setupFELIX; flx-info fpga;flx-info fpga -c1"
# done

# setupFELIX=source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh

for i in {0..15}; do
# for i in {1..1}; do
    printf -v s "%02d" $i
    echo stgc$s
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-stgc-$s "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-info fpga; flx-info fpga -c1" | grep Temperature
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-stgc-$s "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-info fpga; flx-info fpga -c1" | grep Fan
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-stgc-$s "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-info ; flx-info  -c1" | grep "GIT commit number"
    echo
done


for i in {0..11}; do
# for i in {7..7}; do
    printf -v s "%02d" $i
    echo mm$s
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-mm-$s   "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-info fpga; flx-info fpga -c1"  | grep Temperature
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-mm-$s   "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-info fpga; flx-info fpga -c1"  | grep Fan
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-mm-$s   "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-info ; flx-info  -c1"  | grep "GIT commit number"
    ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-mm-$s   "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-config -E list | grep -E 'DMA|LATCH' ; flx-dma-stat" 
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-mm-$s   "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-config get TTC_DEC_CTRL_MASTER_BUSY -d0;  flx-config get TTC_DEC_CTRL_MASTER_BUSY -d1; flx-config get TTC_DEC_CTRL_MASTER_BUSY -d2; flx-config get TTC_DEC_CTRL_MASTER_BUSY -d3; "  | grep TTC_DEC_CTRL_MASTER_BUSY
    # ssh -o StrictHostKeyChecking=no  -t -t pc-tdq-flx-nsw-mm-$s   "source /sw/atlas/felix/felix-04-02-00-b4-stand-alone/x86_64-centos7-gcc8-opt/setup.sh; flx-config get BUSY_MAIN_OUTPUT_FIFO_THRESH_BUSY_ENABLE -d0;  flx-config get BUSY_MAIN_OUTPUT_FIFO_THRESH_BUSY_ENABLE -d1; flx-config get BUSY_MAIN_OUTPUT_FIFO_THRESH_BUSY_ENABLE -d2; flx-config get BUSY_MAIN_OUTPUT_FIFO_THRESH_BUSY_ENABLE -d3; "  | grep BUSY_MAIN_OUTPUT_FIFO_THRESH
    echo
done
