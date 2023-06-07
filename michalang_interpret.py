import sys
from machine import *
f = open(str(sys.argv[1]), "r")
prog = f.read()
print(execute_program(prog), end='')