from sudocool.solve.square_set_collection import ColumnList, RowList, SectionList, SquareList


class Board():
    def __init__(self):
        self.squareList = SquareList()
        self.rowList = RowList()
        self.colList = ColumnList()
        self.sectionList = SectionList()

    def _populate(self):
        self.rowList.getSquares(self.squareList)
        self.colList.getSquares(self.squareList)
        self.sectionList.getSquares(self.squareList)

    def populateByRow(self, sudocooldata):
        self.squareList.populateByRow(sudocooldata)
        self._populate()

    def populateBySection(self, sudocooldata):
        self.squareList.populateBySection(sudocooldata)
        self._populate()

    def solved(self):
        """Has the board been solved?"""
        return self.rowList.solved() and self.colList.solved() and self.sectionList.solved()

    def inconsistent(self):
        """Is the board in an inconsistent state?

        The board is in an inconsistent state if there remain any squares that have
        no possibilities left but that haven't been marked as solved"""

        unsolved_squares = [
            square for i, square in enumerate(self.squareList.squares)
            if not square.solved and len(square.possibilities) == 0]

        return len(unsolved_squares) > 0

    def printByRow(self):
        board_rows = []
        for row in self.rowList.items:
            row_squares = [str(square.value) for square in row.squares]
            board_rows.append(",".join(row_squares))

        return ",".join(board_row for board_row in board_rows)

    def printBySection(self):
        board_sections = []
        for section in self.sectionList.items:
            section_squares = [str(square.value) for square in section.squares]
            board_sections.append(",".join(section_squares))

        return ",".join(board_section for board_section in board_sections)
