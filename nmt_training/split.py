'''
    Script to split data into pairs
'''

import sys

for data in ["train", "dev", "test"]:
    src = open(f"{data}.jpn", "w+")
    tgt = open(f"{data}.eng", "w+")
    with open(data, "r") as f:
        for line in f:
            line = line.strip()
            line = line.split("\t")
            a, b = line
            src.write(b+"\n")
            tgt.write(a+"\n")
    src.close()
    tgt.close()