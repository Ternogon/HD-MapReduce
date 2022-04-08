#!/usr/bin/python3

import sys

for line in sys.stdin:
    collection = line.lower().strip('\r\n ').split(",")
    
    for item in collection:    
        H = {}
        for item2 in collection:        
            if item2 in H:
                H[item2] += 1
                
            else:
                H[item2] = 1
            
        print("{}--{}".format(item, H))
