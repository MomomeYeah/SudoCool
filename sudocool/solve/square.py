import math


class Square:
    """Class representing a single square on the Sudoku board.

    Each square knows what row, column, and section it is in, as well as the
    set of numbers that it could still possibly be set to.
    """

    def __init__(self, row, col, value):
        self.row = int(row)
        self.col = int(col)
        self.section = int(math.floor(col / 3) + 3*math.floor(row / 3))
        if value != None and value != '':
            self.value = int(value)
            self.solved = True
            self.possibilities = None
        else:
            self.value = ''
            self.solved = False
            self.possibilities = list(range(1,10))

    def __str__(self):
        possibilities = ",".join(str(i) for i in self.possibilities)
        return "Row: {}, Column: {}, ".format(self.row, self.col) +\
            "Section: {}, Value: {}, ".format(self.section, self.value) +\
            "Solved: {}, Possibilities: {}".format(self.solved, possibilities)

    def removePossibility(self, possibility):
        if not self.solved and possibility in self.possibilities:
            self.possibilities.remove(possibility)

    def removePossibilities(self, possibilities):
        for possibility in possibilities:
            self.removePossibility(possibility)

    def solve(self, possibility):
        self.solved = True
        self.value = possibility
        self.possibilities = None

    def hasPossibility(self, possibility):
        return self.solved == False and possibility in self.possibilities

    def hasPartialIntersect(self, possibilities):
        return self.possibilities != possibilities and set(self.possibilities) & set(possibilities)
