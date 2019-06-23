#!/usr/bin/env python
#	sourcefile: tempasm.py
#	author: kjp@kellyfx.com
#	desc: converts assembly template file into an assembly code generator python script, then runs it
#           ultimate purpose is to make asm() function from assembly, probably from .lss
#           yes this is a code generator that creates code generators

#from argparse import ArgumentParser, FileType
import argparse
import re, sys, string

def main():
    header = '#!/usr/bin/env python\n#autogenerated from %s\nimport sys\nimport asmbits\n'
    fnbegin = '(r"""'
    prbegin = 'sys.stdout.write(r"""'
    prendnoformat = '""")\n'
    prendinsection = '""".format(**locals()))\n'
    argparser = argparse.ArgumentParser(description='Template engine for assembly code')
    argparser.add_argument('sourcefile', help='blah.s', type=argparse.FileType('r'))
    indent = 0
    with argparser.parse_args().sourcefile as f:
        src = f.readlines()
    with open('tmpxme.py', mode='w') as dest:
        dest.write(header % argparser.parse_args().sourcefile.name)
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
                if lineparse.group(1) == '\\':      # python indent +1 level
                    statement = lineparse.group(2)
                    if statement == '':
                        statement = 'if 1:'         # faking an indent, hakception for simply interpret the text
                    dest.write(' '*indent + statement)
                    if statement[-1] == ':':        # is this indent or function
                        dest.write('\n')
                        insidesect = True
                    else:
                        dest.write(fnbegin)
                        insideprint = True
                    indent += 4
                if lineparse.group(1) == '/':       # python unindent 1 level
                    indent -= 4
                    if indent <= 0:
                        indent = 0
                        insidesect = False
                if lineparse.group(1) == '>':       # insert python command
                    dest.write(' '*indent + lineparse.group(2)+'\n')
                if lineparse.group(1) == '}':       # start of python code section
                    insidecode = False
                if lineparse.group(1) == '{':       # end of python code section
                    insidecode = True
            else:
                if not insideprint and not insidecode:
                    dest.write(' '*indent + prbegin)
                    insideprint = True
                dest.write(line)
        if insideprint:
            dest.write(prendnoformat)
    import tmpxme

if __name__ == "__main__":
    main()
