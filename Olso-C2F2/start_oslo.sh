#!/bin/bash
echo start_oslo
adb wait-for-device
adb root;

#locate the spi bus
out=`adb shell ls /d/iaxxx`
for word in $out; do
  if [[ "$word" ==  "spi"* ]]
  then
    port="$word"
    echo "$port found"
  fi
done

#wait for Athletico to start
adb shell 'echo 0x0d000008 > /d/iaxxx/'$port'/address'
adb shell 'echo 1 > /d/iaxxx/'$port'/count'

value=`adb shell 'cat /d/iaxxx/'$port'/data'`
echo "$value"
while [ "$value" != "0D000000: -------- -------- 00000001" ]
do
  adb shell oslo_config_test -r 1 # retry setting the route
  value=`adb shell 'cat /d/iaxxx/'$port'/data'`
  echo "$value"
  sleep 1
done
