# pyasm
a compiler written in python

pyasm.py is a compiler that turns tiao.pa into assembly, out.asm

tiao.py ,tiao.c, tiao.pa all solve the same problem:

moving a point on a 6*5 chess board in a L shape(one direction two steps, the other direction one step)

can the point get back to the original point reaching every other point once and only once?

tiao.c is translated by hand from tiao.py, and tiao.pa is translated by hand from tiao.c

example.pa is a reminder of the grammer of .pa files

i wrote this to understand how a program works in the lower level and how compilers(like gcc) works

i learned how to program in nasm from https://cs.lmu.edu/~ray/notes/nasmtutorial/
