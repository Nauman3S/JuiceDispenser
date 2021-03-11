#!/bin/bash
PID="$(pidof matchbox-keyboard)"
if [  "$PID" != ""  ]; then
  kill $PID
else
sudo DISPLAY=:1.0 matchbox-keyboard  &
sleep 0.6
sudo DISPLAY=:1.0 wmctrl -r "Keyboard" -b add,above
fi