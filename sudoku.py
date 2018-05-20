#!/usr/bin/python

# Sudoku puzzle solver using the Z3 SMT solver.
# Example done to exercise python programming and learn about SMT solvers
# By Luis Grangeia 

import sys
from z3 import *

def create_pos():
    # creates a simple coordinate dictionary to map sudoku coordinates to an array:
    c = {}
    i = 0
    for x in 'ABCDEFGHI':
        for y in xrange(1,10):
            y = str(y)
            c[x+y] = i
            i += 1
    return c

def pretty_print(puzzle):
    for y in xrange(9):
        print '{} {} {}|{} {} {}|{} {} {}'.format(*puzzle[y*9:y*9+9])
        if y == 2 or y == 5:
            print "- - -+- - -+- - -"

def solve_puzzle(puzzle):
    s = Solver()

    # inside this function we will use a dictionary to map coordinates to values in the sudoku board
    sk = {}

    for x in 'ABCDEFGHI':
        for y in xrange(1,10):
            y = str(y)
            sk[x+y] = Int(x+y)

    # Constraints for ALL Sudoku Puzzles
    # Constraint 0: All numbers are between 1 and 9:
    for x in sk:
        s.add (sk[x] > 0)
        s.add (sk[x] < 10)

    # Constraint 1: all lines must be different:
    for x in 'ABCDEFGHI':
        s.add(Distinct([sk[x+str(y)] for y in xrange(1,10)]))

    # Constraint 2: all columns must be different:
    for y in xrange(1,10):
        s.add(Distinct([sk[x+str(y)] for x in 'ABCDEFGHI']))

    # Constraint 3: all 3x3 squares must be distinct:
    sq1 = ('A1','A2','A3','B1','B2','B3','C1','C2','C3')
    sq2 = ('A4','A5','A6','B4','B5','B6','C4','C5','C6')
    sq3 = ('A7','A8','A9','B7','B8','B9','C7','C8','C9')
    sq4 = ('D1','D2','D3','E1','E2','E3','F1','F2','F3')
    sq5 = ('D4','D5','D6','E4','E5','E6','F4','F5','F6')
    sq6 = ('D7','D8','D9','E7','E8','E9','F7','F8','F9')
    sq7 = ('G1','G2','G3','H1','H2','H3','I1','I2','I3')
    sq8 = ('G4','G5','G6','H4','H5','H6','I4','I5','I6')
    sq9 = ('G7','G8','G9','H7','H8','H9','I7','I8','I9')

    s.add(Distinct([sk[x] for x in sq1]))
    s.add(Distinct([sk[x] for x in sq2]))
    s.add(Distinct([sk[x] for x in sq3]))
    s.add(Distinct([sk[x] for x in sq4]))
    s.add(Distinct([sk[x] for x in sq5]))
    s.add(Distinct([sk[x] for x in sq6]))
    s.add(Distinct([sk[x] for x in sq7]))
    s.add(Distinct([sk[x] for x in sq8]))
    s.add(Distinct([sk[x] for x in sq9]))

    # Constraints for this specific input puzzle:
    pos = create_pos()
    for x in 'ABCDEFGHI':
        for y in xrange(1,10):
            y = str(y)
            c = int(puzzle[pos[x+y]])
            if c != 0:
                s.add(sk[x+y] == c)

    s.check()
    m = s.model()

    solution_array = []
    for x in 'ABCDEFGHI':
        for y in xrange(1,10):
            y = str(y)
            solution_array.append(m.evaluate(sk[x+y]))
    return solution_array


def main():

    if len(sys.argv) != 2:
        print sys.argv[0] + " <puzzle.txt>"
        exit(-1)

    puzzle = []
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        if len(lines) != 9:
            print 'puzzle is badly formed: %s lines of input' % lines
            exit (-1)

        for y in xrange(9):
            l = lines[y].strip()
            cols = l.split();
            if len(cols) != 9:
                print 'puzzle is badly formed: line %s contains %s columns' % (y, len(cols))
                exit(-1)
            for x in xrange(9):
                puzzle.append(cols[x])

    print "Input Puzzle:"
    pretty_print(puzzle)

    solution = solve_puzzle(puzzle)

    print "\nPuzzle Solution:"
    pretty_print(solution)


if __name__ == "__main__":  
    main()
