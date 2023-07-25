opcode  psudo           asm

0       no op           nop
1       zero a          z a
2       zero b          z b
3       zero x          z x
4       zero y          z y
5       swap a, b       swp a, b
6       swap x, y       swp x, y
7       swap a, x       swp a, x
8       swap b, y       swp b, y
9       inc a           inc a
10      inc b           inc b
11      inc x           inc x
12      inc y           inc y
13      dec a           dec a
14      dec b           dec b
15      dec x           dec x
16      dec y           dec y
17      zero mem[arg]   z 000000
18      zero mem[a]     z [a]
19      zero mem[b]     z [b]
20      zero mem[[arg]] z [000000]
21      zero mem[[a]]   z [[a]]
22      zero mem[[b]]   z [[b]]
23      inc mem[arg]    inc 0000000
24      inc mem[a]      inc [a]
25      inc mem[b]      inc [b]
26      inc mem[[arg]]  inc [0000000]
27      inc mem[[a]]    inc [[a]]
28      inc mem[[b]]    inc [[b]]