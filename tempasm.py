#!/usr/bin/env python
#	filename: tempasm.py
#	author: kjp@kellyfx.com
#	desc: converts assembly template file into an assembly code generator python script, then runs it
#           yes this is a code generator that creates code generators

from argparse import ArgumentParser
import re, sys, string

def main():
    header = '#!/usr/bin/env python\n#autogenerated from %s\nimport sys\nimport asmbits\n'
    fnbegin = '(r"""'
    prbegin = 'sys.stdout.write(r"""'
    prendnoformat = '""")\n'
    prendinsection = '""".format(**locals()))\n'
    argparser = ArgumentParser(description='Template engine for assembly code')
    argparser.add_argument('filename', help='blah.s')
    indent = 0
    with open(argparser.parse_args().filename, mode='r') as f:
        src = f.readlines()
    with open('tmpxme.py', mode='w') as dest:
        dest.write(header % argparser.parse_args().filename)
        insideprint = False
        insidesect = False
        insidecode = False
        for line in src:
            lineparse = re.search(r'^\.([>/\\{}])(.*)',line)
            if lineparse:
                if insideprint:     # going from inside to outside (lineparse is outside)
                    insideprint = False
                    if insidesect:
                        dest.write(prendinsection)
                    else:
                        dest.write(prendnoformat)
                if lineparse.group(1) == '\\':    # python indent +1 level
                    dest.write(' '*indent + lineparse.group(2))
                    if lineparse.group(2)[-1] == ':':
                        dest.write('\n')
                        insidesect = True
                    else:
                        dest.write(fnbegin)
                        insideprint = True
                    indent += 4
                if lineparse.group(1) == '/':     # python unindent 1 level
                    insidesect = False
                    indent -= 4
                if lineparse.group(1) == '>':     # insert python command
                    dest.write(' '*indent + lineparse.group(2)+'\n')
                if lineparse.group(1) == '}':     # start of python code section
                    insidecode = False
                if lineparse.group(1) == '{':     # end of python code section
                    insidecode = True
            else:
                if not insideprint and not insidecode:
                    dest.write(' '*indent + prbegin)
                    insideprint = True
                dest.write(line)
        dest.write(prendnoformat)
    import tmpxme

if __name__ == "__main__":
    main()
