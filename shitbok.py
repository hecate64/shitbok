#!/usr/bin/python
#
# Shitbok Interpreter
# implemeted by modifying https://github.com/pocmo/Python-Brainfuck
#
# Usage: ./shitbok.py [FILE]


import sys
import getch

def execute(filename):
  f = open(filename, "r")
  evaluate(f.read())
  f.close()


def evaluate(code):

  code     = cleanup(code)
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < len(code):
    command = code[codeptr]

    if command == "111":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "110":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "101":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "100":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "011" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "010" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == "001": cells[cellptr] = ord(getch.getch())
    if command == "000": sys.stdout.write(chr(cells[cellptr]))
      
    codeptr += 1


def cleanup(code):
  code = ''.join(filter(lambda x: x in ['s','h','i','t','b','o','k'], code))
  code = code.replace('shit', '1')
  code = code.replace('bok' , '0')
  code = [code[i:i+3] for i in range(0, len(code), 3)]
  return code


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "011": temp_bracestack.append(position)
    if command == "010":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def main():
  if len(sys.argv) == 2: execute(sys.argv[1])
  else: print("Usage:", sys.argv[0], "filename")

if __name__ == "__main__": main()

