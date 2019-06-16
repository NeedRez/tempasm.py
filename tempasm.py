#!/usr/bin/env python
#	filename: tempasm.py
#	author: kjp@kellyfx.com
#	desc: converts assembly template file into an assembly code generator python script, then runs it
#           yes this is a code generator that creates code generators

from argparse import ArgumentParser
import re, string

def main():
    prbegin = 'print(r"""'
    prendnoformat = '"""),\n'
    prendinsection = '""".format(**locals())),\n'
    parser = ArgumentParser(description='Template engine for assembly code')
    parser.add_argument('filename', help='blah.s')
    indent = 0
    with open('tmpxme.py', 'w') as d:
        with open(parser.parse_args().filename) as s:
            d.write(prbegin)
            insideprint = True
            insidesect = False
            insidecode = False
            for line in s:
                esc = re.search(r'^\.(.)(.*)',line)
                if esc:
                    if insideprint:     # going from inside to outside (esc is outside)
                        insideprint = False
                        if insidesect:
                            d.write(prendinsection)
                        else:
                            d.write(prendnoformat)
                    if esc.group(1) == '\\':    # python indent +1 level
                        d.write(' '*indent + esc.group(2)+'\n')
                        insidesect = True
                        indent += 4
                    if esc.group(1) == '/':     # python unindent 1 level
                        insidesect = False
                        indent -= 4
                    if esc.group(1) == '>':     # insert python command
                        d.write(' '*indent + esc.group(2)+'\n')
                    if esc.group(1) == '}':     # start of python code section
                        insidecode = False
                    if esc.group(1) == '{':     # end of python code section
                        insidecode = True
                else:
                    if not insideprint and not insidecode:
                        d.write(' '*indent + prbegin)
                        insideprint = True
                    d.write(line)
            d.write(prendnoformat)
    import tmpxme

if __name__ == "__main__":
    main()
