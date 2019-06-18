#!/usr/bin/env python
#	filename: asmbits.py
#	author: kjp@kellyfx.com
#	desc: run-time utilities for bit manipulations, executed from intermediate script tmpxme.py
import re, sys, math

def bitfield(bits):
    match = re.search(r'\[(.*)\](.*)', bits, re.MULTILINE)
    if match.group(1):
        for i, x in enumerate(reversed(match.group(1).split('|'))):
            sys.stdout.write(x.strip())
            sys.stdout.write(match.group(2).format(bitmask=hex(pow(2,i)))+'\n') # should make a class and pass it
