# tempasm.py
Converts a template file into a "code generator" python script, then imports the generator to run the generated code. Example script is shown here:

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

This python script is generated:

          y = '0b1'
          for x in reversed(['bit7','bit6','bit5','bit4','bit3','bit2','bit1','bit0']):
              sys.stdout.write(r"""{x}    .def    {y}
          """.format(**locals()))
          y += '0'
          sys.stdout.write(r"""        ; or call a custom python function that accepts your syntax
          """)
          asmbits.bitfield(r"""[ bit7 | bit6 | bit5 | bit4 | bit3 | bit2 | bit1 | bit0 ]    .def {bitmask}
          """)

The output is here:

                ; bulk-create bit defines using inline python
        bit0    .def    0b1
        bit1    .def    0b10
        bit2    .def    0b100
        bit3    .def    0b1000
        bit4    .def    0b10000
        bit5    .def    0b100000
        bit6    .def    0b1000000
        bit7    .def    0b10000000
                ; or call a custom python function that accepts your syntax
        bit0    .def 0x1
        bit1    .def 0x2
        bit2    .def 0x4
        bit3    .def 0x8
        bit4    .def 0x10
        bit5    .def 0x20
        bit6    .def 0x40
        bit7    .def 0x80
