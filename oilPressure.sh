#!/bin/bash
cd /home/pi/genmon
if test -f userdefined.json; then
  rm userdefined.json
fi
python3 oilPressure.py &
exit 0

