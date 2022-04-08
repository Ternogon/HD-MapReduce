#!/usr/bin/python3

import sys

for line in sys.stdin:
    collection = line.lower().strip('\r\n ').split(",")
    for index_1 in range(len(collection)):
        for index_2 in range(index_1 + 1, len(collection)):
            if collection[index_2] > collection[index_1]:
                print(f'{collection[index_1]}:{collection[index_2]}--1')
            else:
                print(f'{collection[index_2]}:{collection[index_1]}--1')