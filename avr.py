#!/usr/bin/env python
#	file_name_: avr.py
#	author: kjp@kellyfx.com
#	desc: run-time utilities for bit manipulations, executed from intermediate script tmpxme.py
#       this runs during the "print" cycle
#       it's easier to debug if you put your code here
#       TODO: use re.compile

import sys, re

class bitclass:
    def __init__(self, reg):
        pass

mask = bitclass('MASK')
ddr = bitclass('DDR')
port = bitclass('PORT')
pin = bitclass('PIN')

def pdef(signal, pio, bit):
    setattr(ddr, signal, 'DDR{}'.format(pio))
    setattr(port, signal, 'PORT{}'.format(pio))
    setattr(pin, signal, 'PIN{}'.format(pio))
    setattr(mask, signal, 'P{}{}'.format(pio,bit))

def iodef(text):
    msb = 7
    lsb = 0
    pioletter = 'x'
    default = '0,1'     # ddr, port
    for t in re.split(r'[|\r\n]+', text):                           # delimiters are | or EOL
        s = t.format(T='(0,0)', P='(0,1)', L='(1,0)', H='(1,1)',**globals())    # expand the port defs (not sure where these come from yet) 
        pio_name_rgx = re.match(r'([a-zA-Z]\w*)\[(\d*):(\d*)\]',s)  # looking for name before brackets
        if pio_name_rgx:
            pioletter=pio_name_rgx.group(1)
            if pio_name_rgx.group(2):
                msb = int(pio_name_rgx.group(2))
            if pio_name_rgx.group(3):
                lsb = int(pio_name_rgx.group(3))
            s = ''
            bit = msb
        sig_group_rgx = re.match(r'\[([a-zA-Z]\w*)\]',s)            # looking for name in brackets
        if sig_group_rgx:
            sig_name = sig_group_rgx.group(1)   # = 'INITA'
            setattr(ddr, sig_name, 0)
            setattr(port, sig_name, 0)
            s = ''
        sig_name_rgx = re.match(r'([a-zA-Z]\w*)(\s*=\s*\((.*)\))?',s)   # looking for name before optional equals sign (group 3 has params)
        if sig_name_rgx:
            if sig_name_rgx.group(3):
                data = sig_name_rgx.group(3)
            else:
                data = default
            result = [x.strip() for x in data.split(',')]
            if result[0] == '1':
                setattr(ddr, sig_name, getattr(ddr, sig_name) | pow(2,bit))
            if result[1] == '1':
                setattr(port, sig_name, getattr(port, sig_name) | pow(2,bit))
            sys.stdout.write('.def\t{}\tP{}{}\t; (ddr,port)=({})\n'.format(sig_name_rgx.group(1), pioletter, bit, data))
            pdef(sig_name_rgx.group(1), pioletter, bit)
            if bit > lsb:                                           # artifact is the lsb define repeated if too many bits given
                bit -= 1
