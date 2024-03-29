# tempasm.py
Converts a template file into a "code generator" python script, then imports the generator to run the generated code.
# Purpose
Bringing the power of Python to Assembly language generation. Let Python "do the math" so you don't have to remember bits and bytes. I wanted something that would convert some simple GPIO notation into assembly macros. An AVR GPIO port might be defined such as this:
~~~
A[7:0]|[INITA]|AC_DET={T}|RELAY={H}|SCTL3={P}|SCTL2={T}|SCTL1={T}|RXIR={P}|L1_INA={H}|L2_INB={H}
~~~
The tags in brackets eg. {T} are replaced by a list of bits such as (0,0) setting the AVR ddr and port values to be written. Doing this with assembly macros might be possible but really the state of affairs for assemblers these days is not so good. Maybe template engine could work, I didn't like what the result looked like. I started to make my own template engine but rather than only expose little bits of python in the template I would expose the whole system.

With this template engine, essentially Python is now turned "inside-out" where we have a text file with escape characters for python code. This gets converted to Python code including the print statement that puts the text inside quotes. That newly created code is imported to run. The GPIO notation above is given to the avr.iodef Python function as data, the function then sets the appropriate variables for future use (found in the classes such as ddr and port).

# Usage Example
Example script is shown here:

NOTE: this requires avr.py which is in still development
~~~~
.>import avr
.>from avr import ddr, port, pin, mask
.\avr.iodef
A[7:0]
[INITA]
AC_DET={T}
RELAY={H}
SCTL3={P}
SCTL2		;default
SCTL1={T}
RXIR={P}
L1_INA={H}
L2_INB={H}
./
.\
	;signal tags can now be inserted into code
	;{{mask.RELAY}} = {mask.RELAY}
	;{{pin.RELAY}} = {pin.RELAY}
	;{{port.RELAY}} = {port.RELAY}
	;{{ddr.RELAY}} = {ddr.RELAY}

	ldi	r24, 0b{port.INITA:08b}	; uses defined name INITA as preset {{port.INITA}}
	out	PORTA, r24
	ldi	r24, 0b{ddr.INITA:08b}	; {{ddr.INITA}}
	out	DDRA, r24
./
~~~~

This python script is generated:
~~~
#!/usr/bin/env python
#autogenerated from test.s
import sys
import avr
from avr import ddr, port, pin, mask
avr.iodef(r"""A[7:0]
[INITA]
AC_DET={T}
RELAY={H}
SCTL3={P}
SCTL2		;default
SCTL1={T}
RXIR={P}
L1_INA={H}
L2_INB={H}
""")
if 1:
    sys.stdout.write(r"""	;signal tags can now be inserted into code
	;{{mask.RELAY}} = {mask.RELAY}
	;{{pin.RELAY}} = {pin.RELAY}
	;{{port.RELAY}} = {port.RELAY}
	;{{ddr.RELAY}} = {ddr.RELAY}

	ldi	r24, 0b{port.INITA:08b}	; uses defined name INITA as preset {{port.INITA}}
	out	PORTA, r24
	ldi	r24, 0b{ddr.INITA:08b}	; {{ddr.INITA}}
	out	DDRA, r24
""".format(**locals()))
~~~

The output is here:
~~~
.def	AC_DET	PA7	; (ddr,port)=(0,0)
.def	RELAY	PA6	; (ddr,port)=(1,1)
.def	SCTL3	PA5	; (ddr,port)=(0,1)
.def	SCTL2	PA4	; (ddr,port)=(0,1)
.def	SCTL1	PA3	; (ddr,port)=(0,0)
.def	RXIR	PA2	; (ddr,port)=(0,1)
.def	L1_INA	PA1	; (ddr,port)=(1,1)
.def	L2_INB	PA0	; (ddr,port)=(1,1)
	;signal tags can now be inserted into code
	;{mask.RELAY} = PA6
	;{pin.RELAY} = PINA
	;{port.RELAY} = PORTA
	;{ddr.RELAY} = DDRA

	ldi	r24, 0b01110111	; uses defined name INITA as preset {port.INITA}
	out	PORTA, r24
	ldi	r24, 0b01000011	; {ddr.INITA}
	out	DDRA, r24
~~~
