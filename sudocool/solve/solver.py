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

    def singleCandidate(self):
        """If a cell has only one possibility, solve that cell"""

        found = False
        for square in self.board.squareList.squares:
            if not square.solved and len(square.possibilities) == 1:
                found = True
                self.solveSquare(square, square.possibilities[0])
        return found

    def singlePosition(self):
        """
        Solve single-position squares.

        For each possibility in each row / column / section, if there is only
        one cell in that row / column / section containing that possibility, then
        that cell's value can only be that posibility"""

        found = False
        for collectionSet in [self.board.rowList, self.board.colList, self.board.sectionList]:
            # for every row, column, or section
            for collection in collectionSet.items:
                # for each possibility remaining in the collection
                for possibility in collection.possibilities:
                    # find all squares with that possibility
                    squares_with_possibility = [
                        square for square in collection.squares
                        if square.hasPossibility(possibility)]

                    # if there is only one such square, solve the square
                    if len(squares_with_possibility) == 1:
                        found = True
                        self.solveSquare(squares_with_possibility[0], possibility)

        return found

    def candidateLine(self):
        """Remove possibilities based on candidate line test.

        For each possibility in each section, look at all cells in that section
        containing that possibility. If all such cells fall on a single row or
        column, that row or column in that section must contain that possibility.
        Therefore, we can remove that possibility from cells in the same row or
        column in other sections"""

        found = False
        for section in self.board.sectionList.items:
            for possibility in section.possibilities:
                # get all squares in this section containing this possibility
                section_squares_with_possibility = [
                    square for square in section.squares
                    if square.hasPossibility(possibility)]

                # if they all fall on a single row, then remove the possibility
                # from all other squares in the same row in different sections
                rows = set(square.row for square in section_squares_with_possibility)
                if len(rows) == 1:
                    row = self.board.rowList.items[rows.pop()]
                    remove_squares = [
                        square for square in row.squares
                        if square.section != section.index
                        and square.hasPossibility(possibility)
                    ]
                    for remove_square in remove_squares:
                        found = True
                        remove_square.removePossibility(possibility)

                # if they all fall on a single col, then remove the possibility
                # from all other squares in the same row in different sections
                cols = set(square.col for square in section_squares_with_possibility)
                if len(cols) == 1:
                    col = self.board.colList.items[cols.pop()]
                    remove_squares = [
                        square for square in col.squares
                        if square.section != section.index
                        and square.hasPossibility(possibility)
                    ]
                    for remove_square in remove_squares:
                        found = True
                        remove_square.removePossibility(possibility)

        return found

    def doublePair(self):
        """Remove possibilities based on double-pair test.

        For each pair of sections in the same section-row or section-col, look at
        each possibility in turn that they have in common. Look for a possibility
        that occurs in exactly two rows (for a section-row) or cols (for a section-col),
        and the same two rows / cols in both sections. If such a possibility exists,
        it must occur in those two rows / cols in those two sections. Therefore,
        remove it from those two rows / cols in the third section in that section-row / col"""


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

    def nakedTuples(self):
        """Remove possibilities based on naked tuples test.

        For each row / col / section, if any N squares have exactly the same N
        possibilities, then only those N squares in that row / col / section can
        contain those N possibilities.

        For example, if 2 squares in the same section each have only 2 possibilities
        and those possibilities are the same, no other squares in that section can
        have either possibility, so remove those 2 possibilities from all other
        squares in that section"""

        found = False
        for collectionSet in [self.board.rowList, self.board.colList, self.board.sectionList]:
            # for every row, column, or section
            for collection in collectionSet.items:
                # for each unsolved square in the collection
                unsolved_squares = [square for square in collection.squares if not square.solved]
                for unsolved_square in unsolved_squares:
                    # get the list of squares in the same collection that have
                    # an identical set of possibilities
                    squares_sharing_possibilities = [
                        square for square in collection.squares
                        if square is not unsolved_square
                        and not square.solved
                        and square.possibilities == unsolved_square.possibilities
                    ]
                    # if the number of shares sharing the set of possibilities
                    # is the same as the number of possibilities, then remove
                    # all those possibilities from all other squares in the
                    # collection
                    if len(squares_sharing_possibilities) == len(unsolved_square.possibilities):
                        remove_squares = [
                            square for square in collection.squares
                            if square is not unsolved_square
                            and not square.solved
                            and square.hasPartialIntersect(unsolved_square)
                        ]
                        for remove_square in remove_squares:
                            found = True
                            remove_square.removePossibilities(unsolved_square.possibilities)

        return found

    def solveRound(self):
        """Attempt to solve the board via all known logical methods.

        Solving functions are called in an infinite loop until none of them
        manage to remove any possibilities from any cells."""

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
                if b_working.solve():
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
