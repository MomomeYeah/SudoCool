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
            # for each section, get a list of sections in the same section-row
            same_row_sections = [
                test_section for test_section in self.board.sectionList.items
                if test_section.rowIndex == section.rowIndex
                and test_section.colIndex != section.colIndex
            ]
            for same_row_section in same_row_sections:
                section_cols = [section.colIndex, same_row_section.colIndex]
                for possibility in section.possibilities:
                    section_possibility_rows = section.getRowsContainingPossibility(possibility)
                    same_row_section_possibility_rows = same_row_section.getRowsContainingPossibility(possibility)

                    if len(section_possibility_rows) == 2 and section_possibility_rows == same_row_section_possibility_rows:
                        remove_sections = [
                            remove_section for remove_section in self.board.sectionList.items
                            if remove_section.rowIndex == section.rowIndex
                            and remove_section.colIndex not in section_cols
                        ]
                        for remove_section in remove_sections:
                            remove_squares = [
                                square for square in remove_section.squares
                                if square.row in section_possibility_rows
                                and square.hasPossibility(possibility)
                            ]
                            for remove_square in remove_squares:
                                found = True
                                remove_square.removePossibility(possibility)

            # for each section, get a list of sections in the same section-col
            same_col_sections = [
                test_section for test_section in self.board.sectionList.items
                if test_section.colIndex == section.colIndex
                and test_section.rowIndex != section.rowIndex
            ]
            for same_col_section in same_col_sections:
                section_rows = [section.rowIndex, same_col_section.rowIndex]
                for possibility in section.possibilities:
                    section_possibility_cols = section.getColsContainingPossibility(possibility)
                    same_col_section_possibility_cols = same_col_section.getColsContainingPossibility(possibility)

                    if len(section_possibility_cols) == 2 and section_possibility_cols == same_col_section_possibility_cols:
                        remove_sections = [
                            remove_section for remove_section in self.board.sectionList.items
                            if remove_section.colIndex == section.colIndex
                            and remove_section.rowIndex not in section_rows
                        ]
                        for remove_section in remove_sections:
                            remove_squares = [
                                square for square in remove_section.squares
                                if square.col in section_possibility_cols
                                and square.hasPossibility(possibility)
                            ]
                            for remove_square in remove_squares:
                                found = True
                                remove_square.removePossibility(possibility)

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
        """Brute-force a solution to the board.

        For each square that is not yet solved, pick a remaining possibility for
        that square, and attempt to solve the rest of the board with that possibility
        set. If this ultimately results in a solved board, then we're done.
        Otherwise, move on to the next possibility and keep guessing."""

        unsolved_squares = [square for square in self.board.squareList.squares if not square.solved]
        for square in unsolved_squares:
            for possibility in square.possibilities:
                bs_working = copy.deepcopy(self)
                bs_working.solveSquare(square, possibility)
                if bs_working.solve():
                    return bs_working.board
                else:
                    square.removePossibility(possibility)

        return self.board

    def solve(self):
        self.solveRound()

        if self.board.solved():
            return True
        elif self.board.inconsistent():
            return False

        guessed_board = self.guess()
        if guessed_board.inconsistent():
            return False
        elif not guessed_board.solved():
            return False
        else:
            self.board = guessed_board
            return True

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
