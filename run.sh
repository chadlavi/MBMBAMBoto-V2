#!/bin/bash
until `python2 mbmbamboto.py`; do
    echo "'mbmbamboto.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
