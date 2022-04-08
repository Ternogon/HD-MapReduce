#!/usr/bin/python3

import sys

(lastKey, s) = (None, "{}")

s = eval(s)
for line in sys.stdin:
    (key, value) = line.replace('\r\n ', '').split("--")
    value = eval(value)
    if lastKey and lastKey != key:
        print(f'{lastKey}:', end='')
        for i, j in s.items():
            if i == lastKey:
                continue 
            print(f'{i}={j}', end=';')
        print()
        (lastKey, s) = (key, value)
    else:
        for i in value:
            s[i] = s[i] + value[i] if i in s else value[i]
        lastKey = key
