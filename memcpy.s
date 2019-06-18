.{
def nop(i):
    for x in range(1,i):
        sys.stdout.write('\tnop\t; {x}\n'.format(x=x))
.}
loop16:
        ldr    	r12, [r1], #4
.>nop(10)
.macro  hi
1:      mov    	r4, r12
	ldmia	r1!, {   r5,r6,r7,  r8,r9,r10,r11}
        subs   	r2, r2, #32

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
.\for x, y in zip(['loop16','loop8','loop24'], ['16','24','8']):
{x}:
        ldr    	r12, [r1], #4
1:      mov    	r4, r12
	ldmia	r1!, {{   r5,r6,r7,  r8,r9,r10,r11}}
        subs   	r2, r2, #32
        ldrhs  	r12, [r1], #4
.>items = ['r3','r4','r5','r6','r7','r8','r9']
.\for a, b in zip(items, items[1:]):
        orr     {a}, {a}, {b}, lsl #{y}
        mov     {b}, {b}, lsr #{y}
./
        orr	r9, r9, r10, lsl #{y}
        mov	r10, r10,		lsr #{y}
        orr	r10, r10, r11, lsl #{y}
        stmia	r0!, {{r3,r4,r5,r6, r7,r8,r9,r10}}
        mov	r3, r11, lsr #{y}
        bhs	1b
        b	less_than_thirtytwo
./
        ; or do it the hard way
