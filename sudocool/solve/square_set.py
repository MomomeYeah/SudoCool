import math


class SquareSet:
    """Generic base class for a collection of squares. This collection will be
    either a row, column, or section
    """

    def __init__(self, index):
        self.index = index
        self.possibilities = list(range(1,10))
        self.squares = []

    def __str__(self):
        possibilities = ",".join(str(i) for i in self.possibilities)
        return "Index: {}, Possibilities: {}".format(self.index, possibilities)

    def __eq__(self, index):
        return self.index == index

    def solved(self):
        return len(self.possibilities) == 0

    def removePossibility(self, possibility):
        if possibility in self.possibilities:
            self.possibilities.remove(possibility)

class Row(SquareSet):
    pass

class Column(SquareSet):
    pass

class Section(SquareSet):
    def __init__(self, index):
        super().__init__(index)
        self.rowIndex = int(math.floor(index / 3))
        self.colIndex = index % 3

    def __str__(self):
        possibilities = ",".join(str(i) for i in self.possibilities)
        return "Index: {}, Row Index: {}, Column Index: {}, Possibilities: {}".format(
            self.index, self.rowIndex, self.colIndex, possibilities)
