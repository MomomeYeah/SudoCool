import math

from sudocool.solve.square import Square
from sudocool.solve.square_set import Column, Row, Section


class SquareSetList:
    def __init__(self, item_class):
        self.items = []
        for i in range(9):
            self.items.append(item_class(i))

    def getSquares(self, squareList, attr_name):
        for square in squareList.squares:
            square_set = self.items[getattr(square, attr_name)]
            square_set.squares.append(square)

    def removePossibility(self, index, possibility):
        r = self.items[self.items.index(index)]
        r.removePossibility(possibility)

    def solved(self):
        unsolved_items = [item for i, item in enumerate(self.items) if not item.solved()]
        return len(unsolved_items) == 0

class RowList(SquareSetList):
    def __init__(self):
        super().__init__(item_class=Row)

    def getSquares(self, squareList):
        super().getSquares(squareList, "row")

class ColumnList(SquareSetList):
    def __init__(self):
        super().__init__(item_class=Column)

    def getSquares(self, squareList):
        super().getSquares(squareList, "col")

class SectionList(SquareSetList):
    def __init__(self):
        super().__init__(item_class=Section)

    def getSquares(self, squareList):
        super().getSquares(squareList, "section")

class SquareList(object):
    def __init__(self):
        self.squares = []

    def populateByRow(self, sudocooldata):
        for i, val in enumerate(sudocooldata.split(',')):
            self.squares.append(Square(row=math.floor(i/9), col=i%9, value=val))

    def populateBySection(self, sudocooldata):
        sudocooldata_values = sudocooldata.split(',')
        for section in range(9):
            start_index = section * 9
            end_index = start_index + 9
            sudocooldata_section = sudocooldata_values[start_index:end_index]

            for i, val in enumerate(sudocooldata_section):
                row = math.floor(i / 3) + 3 * math.floor(section / 3)
                col = (i % 3) + 3 * (section % 3)

                self.squares.append(Square(row=row, col=col, value=val))

    def removePossibility(self, row, col, section, possibility):
        for square in self.squares:
            if square.row == row or square.col == col or square.section == section:
                square.removePossibility(possibility)

    def solveAndRemovePossibility(self, row, col, section, possibility):
        for square in self.squares:
            if square.row == row and square.col == col:
                square.solve(possibility)
            elif square.row == row and not square.col == col:
                square.removePossibility(possibility)
            elif not square.row == row and square.col == col:
                square.removePossibility(possibility)
            elif not square.row == row and not square.col == col and square.section == section:
                square.removePossibility(possibility)
