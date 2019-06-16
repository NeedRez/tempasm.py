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
    argparser = ArgumentParser(description='Template engine for assembly code')
    argparser.add_argument('filename', help='blah.s')
    indent = 0
    with open('tmpxme.py', 'w') as d:
        with open(argparser.parse_args().filename) as s:
            d.write(prbegin)
            insideprint = True
            insidesect = False
            insidecode = False
            for line in s:
                lineparse = re.search(r'^\.([>/\\{}])(.*)',line)
                if lineparse:
                    if insideprint:     # going from inside to outside (lineparse is outside)
                        insideprint = False
                        if insidesect:
                            d.write(prendinsection)
                        else:
                            d.write(prendnoformat)
                    if lineparse.group(1) == '\\':    # python indent +1 level
                        d.write(' '*indent + lineparse.group(2)+'\n')
                        insidesect = True
                        indent += 4
                    if lineparse.group(1) == '/':     # python unindent 1 level
                        insidesect = False
                        indent -= 4
                    if lineparse.group(1) == '>':     # insert python command
                        d.write(' '*indent + lineparse.group(2)+'\n')
                    if lineparse.group(1) == '}':     # start of python code section
                        insidecode = False
                    if lineparse.group(1) == '{':     # end of python code section
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
