#!/usr/bin/python3
import sys

(lastKey, sum) = (None, 0)

for line in sys.stdin:
    (key, value) = line.replace('\r\n ', '').split("--")

    if lastKey and lastKey != key:
        print(lastKey + '\t' + str(sum))
        (lastKey, sum) = (key, int(value))
    else:
        (lastKey, sum) = (key, sum + int(value))
