#
# make clean; make FRAME_SAMPLES=128 VELOCITY_BINS=16 V10=1 STDIN=1

cat $1 | ./demux_jaws 2> /dev/null | ./impulse_detector_128 2> /dev/null

