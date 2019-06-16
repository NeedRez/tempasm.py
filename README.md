# tempasm.py
Converts a template file into a "code generator" python script, then imports the generator to run the generated code

                  ; bulk-create bit defines using inline python
         .>y = '0b1'
         .\for x in reversed(['bit7','bit6','bit5','bit4','bit3','bit2','bit1','bit0']):
         {x}    .def    {y}
         .>y += '0'
         ./
                  ; or call a custom python function that accepts your syntax
         .\asmbits.bitfield
         [ bit7 | bit6 | bit5 | bit4 | bit3 | bit2 | bit1 | bit0 ]    .def {bitmask}
         ./

creates this python script:

          y = '0b1'
          for x in reversed(['bit7','bit6','bit5','bit4','bit3','bit2','bit1','bit0']):
              sys.stdout.write(r"""{x}    .def    {y}
          """.format(**locals()))
          y += '0'
          sys.stdout.write(r"""        ; or call a custom python function that accepts your syntax
          """)
          asmbits.bitfield(r"""[ bit7 | bit6 | bit5 | bit4 | bit3 | bit2 | bit1 | bit0 ]    .def {bitmask}
          """)
