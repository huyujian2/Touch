#
# make clean; make FRAME_SAMPLES=256 VELOCITY_BINS=8 V10=1 STDIN=1

cat $1 | ./demux_jaws 2> /dev/null | ./impulse_detector_256 2> /dev/null 

