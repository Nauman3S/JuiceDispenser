#!/bin/bash
PID="$(pidof matchbox-keyboard)"
if [  "$PID" != ""  ]; then
  kill $PID
else
 matchbox-keyboard &
 sleep 0.6
 wmctrl -r "Keyboard" -b add,above
fi