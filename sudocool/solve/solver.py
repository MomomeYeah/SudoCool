import copy

from sudocool.solve.board import Board


class BoardSolver():
    def __init__(self, board):
        self.board = board
        self.setupBoard()

    def setupBoard(self):
        for square in self.board.squareList.squares:
            if square.solved:
                self.board.rowList.removePossibility(square.row, square.value)
                self.board.colList.removePossibility(square.col, square.value)
                self.board.sectionList.removePossibility(square.section, square.value)
                self.board.squareList.removePossibility(square.row, square.col, square.section, square.value)

    def solveSquare(self, square, possibility):
        self.board.rowList.removePossibility(square.row, possibility)
        self.board.colList.removePossibility(square.col, possibility)
        self.board.sectionList.removePossibility(square.section, possibility)
        self.board.squareList.solveAndRemovePossibility(square.row, square.col, square.section, possibility)

    # If a cell has only one possibility, solve that cell
    def singleCandidate(self):
        found = False
        for square in self.board.squareList.squares:
            if not square.solved and len(square.possibilities) == 1:
                found = True
                self.solveSquare(square, square.possibilities[0])
        return found

    # For each possibility in each row/col/section, if there is only one cell in that row/col/section containing that possibility, solve that cell
    def singlePosition(self):
        found = False
        for row in self.board.rowList.items:
            for possibility in row.possibilities:
                squares = [square for i, square in enumerate(self.board.squareList.squares) if square.row == row.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    self.solveSquare(squares[0], possibility)
        for col in self.board.colList.items:
            for possibility in col.possibilities:
                squares = [square for i, square in enumerate(self.board.squareList.squares) if square.col == col.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    self.solveSquare(squares[0], possibility)
        for section in self.board.sectionList.items:
            for possibility in section.possibilities:
                squares = [square for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    self.solveSquare(squares[0], possibility)
        return found

    # For each possibility in each section, look at all cells in that section containing that possibility
    # If all such cells fall on a single row or column, that row or column in that section must contain that possibility
    # Therefore, we can remove that possibility from cells in the same row or column in other sections
    def candidateLine(self):
        found = False
        for section in self.board.sectionList.items:
            for possibility in section.possibilities:
                rows = set([square.row for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                if len(rows) == 1:
                    for remove_square in [square for i, square in enumerate(self.board.squareList.squares) if square.section != section.index and square.row in rows and square.hasPossibility(possibility)]:
                        found = True
                        remove_square.removePossibility(possibility)
                cols = set([square.col for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                if len(cols) == 1:
                    for remove_square in [square for i, square in enumerate(self.board.squareList.squares) if square.section != section.index and square.col in cols and square.hasPossibility(possibility)]:
                        found = True
                        remove_square.removePossibility(possibility)
        return found

    # For each pair of sections in the same section-row or section-col, look at each possibility in turn that they have in common
    # Look for a possibility that occurs in exactly two rows (for a section-row) or cols (for a section-col), and the same two rows/cols in both sections
    # If such a possibility exists, it must occur in those two rows/cols in those two sections
    # Therefore, remove it from those two rows/cols in the third section in that section-row/col
    def doublePair(self):
        found = False
        for section in self.board.sectionList.items:
            for test_section in [s for i, s in enumerate(self.board.sectionList.items) if s.rowIndex == section.rowIndex and s.colIndex != section.colIndex]:
                cols = [section.colIndex, test_section.colIndex]
                for possibility in section.possibilities:
                    s_rows = set([square.row for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                    ts_rows = set([square.row for i, square in enumerate(self.board.squareList.squares) if square.section == test_section.index and square.hasPossibility(possibility)])
                    if len(s_rows) == 2 and s_rows == ts_rows:
                        for remove_sections in [s for i, s in enumerate(self.board.sectionList.items) if s.rowIndex == section.rowIndex and not s.colIndex in cols]:
                            for remove_squares in [s for i, s in enumerate(self.board.squareList.squares) if s.section == remove_sections.index and s.row in s_rows and s.hasPossibility(possibility)]:
                                found = True
                                remove_squares.removePossibility(possibility)
            for test_section in [s for i, s in enumerate(self.board.sectionList.items) if s.colIndex == section.colIndex and s.rowIndex != section.rowIndex]:
                rows = [section.rowIndex, test_section.rowIndex]
                for possibility in section.possibilities:
                    s_cols = set([square.col for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                    ts_cols = set([square.col for i, square in enumerate(self.board.squareList.squares) if square.section == test_section.index and square.hasPossibility(possibility)])
                    if len(s_cols) == 2 and s_cols == ts_cols:
                        for remove_sections in [s for i, s in enumerate(self.board.sectionList.items) if s.colIndex == section.colIndex and not s.rowIndex in rows]:
                            for remove_squares in [s for i, s in enumerate(self.board.squareList.squares) if s.section == remove_sections.index and s.col in s_cols and s.hasPossibility(possibility)]:
                                found = True
                                remove_squares.removePossibility(possibility)
        return found

    # For each row/col/section, look through all squares in that row/col/section
    # If any N squares have exactly the same N possibilities, only those N squares in that row/col/section can contain those N possibilities
    # For example if two square share the same two possibilities, those two squares must contain those two possibilities, and no other squares in that row can have either possibility
    # Therefore, remove those N possibilities from all other squares in that row/col/section
    def nakedTuples(self):
        found = False
        for row in self.board.rowList.items:
            for test_square in [square for i, square in enumerate(self.board.squareList.squares) if square.row == row.index and not square.solved]:
                match_squares = [square for i, square in enumerate(self.board.squareList.squares) if square.row == row.index and not square.solved and square.possibilities == test_square.possibilities]
                if len(match_squares) == len(test_square.possibilities):
                    for remove_square in [square for i, square in enumerate(self.board.squareList.squares) if square.row == row.index and not square.solved and square.hasPartialIntersect(test_square.possibilities)]:
                        found = True
                        remove_square.removePossibilities(test_square.possibilities)
        for col in self.board.colList.items:
            for test_square in [square for i, square in enumerate(self.board.squareList.squares) if square.col == col.index and not square.solved]:
                match_squares = [square for i, square in enumerate(self.board.squareList.squares) if square.col == col.index and not square.solved and square.possibilities == test_square.possibilities]
                if len(match_squares) == len(test_square.possibilities):
                    for remove_square in [square for i, square in enumerate(self.board.squareList.squares) if square.col == col.index and not square.solved and square.hasPartialIntersect(test_square.possibilities)]:
                        found = True
                        remove_square.removePossibilities(test_square.possibilities)
        for section in self.board.sectionList.items:
            for test_square in [square for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and not square.solved]:
                match_squares = [square for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and not square.solved and square.possibilities == test_square.possibilities]
                if len(match_squares) == len(test_square.possibilities):
                    for remove_square in [square for i, square in enumerate(self.board.squareList.squares) if square.section == section.index and not square.solved and square.hasPartialIntersect(test_square.possibilities)]:
                        found = True
                        remove_square.removePossibilities(test_square.possibilities)
        return found

    def solveRound(self):
        found = True
        while found:
            found = False
            found = self.singleCandidate()
            if not found:
                found = self.singlePosition()
            if not found:
                found = self.candidateLine()
            if not found:
                found = self.doublePair()
            if not found:
                found = self.nakedTuples()

    def guess(self):
        unsolved_squares = [square for i, square in enumerate(self.board.squareList.squares) if not square.solved]
        for square in unsolved_squares:
            for possibility in square.possibilities:
                b_working = copy.deepcopy(self)
                b_working.solveSquare(square, possibility)
                if b_working.solveBoard():
                    self.solveSquare(square, possibility)
                    return True
                else:
                    square.removePossibility(possibility)
        return False

    def solve(self):
        self.solveRound()

        if self.board.solved():
            return True
        elif self.board.inconsistent():
            return False

        result = True
        while result:
            result = self.guess()

    def __str__(self):
        ret_str = "\nRows:\n\n"
        ret_str += "\n".join(str(r) for r in self.board.rowList.items)
        ret_str += "\n\nCols:\n\n"
        ret_str += "\n".join(str(c) for c in self.board.colList.items)
        ret_str += "\n\nSections:\n\n"
        ret_str += "\n".join(str(s) for s in self.board.sectionList.items)
        ret_str += "\n\nSquares:\n\n"
        ret_str += "\n".join(str(s) for s in self.board.squareList.squares)
        return ret_str
