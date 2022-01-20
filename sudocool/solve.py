import math
import copy

class square(object):
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
        ret_str = "Row: "+str(self.row)+", Col: "+str(self.col)+", Section: "+str(self.section)
        ret_str += ", Value: "+str(self.value)+", Solved: "+str(self.solved)+", "
        if self.possibilities:
            ret_str += ",".join(str(i) for i in self.possibilities)
        return ret_str

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

class rowColOrSection(object):
    def __init__(self, index):
        self.index = index
        self.possibilities = list(range(1,10))

    def __str__(self):
        return "Index: "+str(self.index)+", Possibilities: "+",".join(str(i) for i in self.possibilities)

    def __eq__(self, index):
        return self.index == index

    def solved(self):
        return len(self.possibilities) == 0

    def removePossibility(self, possibility):
        if possibility in self.possibilities:
            self.possibilities.remove(possibility)

class section(rowColOrSection):
    def __init__(self, index):
        rowColOrSection.__init__(self, index)
        self.rowIndex = int(math.floor(index / 3))
        self.colIndex = index % 3

    def __str__(self):
        return "Index: "+str(self.index)+", Row Index: "+str(self.rowIndex)+", Col Index: "+str(self.colIndex)+", Possibilities: "+",".join(str(i) for i in self.possibilities)

class rowList(object):
    def __init__(self):
        self.rows = []
        for i in range(9):
            self.rows.append(rowColOrSection(i))

    def removePossibility(self, index, possibility):
        r = self.rows[self.rows.index(index)]
        r.removePossibility(possibility)

    def solved(self):
        unsolved_rows = [row for i, row in enumerate(self.rows) if not row.solved()]
        return len(unsolved_rows) == 0

class colList(object):
    def __init__(self):
        self.cols = []
        for i in range(9):
            self.cols.append(rowColOrSection(i))

    def removePossibility(self, index, possibility):
        c = self.cols[self.cols.index(index)]
        c.removePossibility(possibility)

    def solved(self):
        unsolved_cols = [col for i, col in enumerate(self.cols) if not col.solved()]
        return len(unsolved_cols) == 0

class sectionList(object):
    def __init__(self):
        self.sections = []
        for i in range(9):
            self.sections.append(section(i))

    def removePossibility(self, index, possibility):
        s = self.sections[self.sections.index(index)]
        s.removePossibility(possibility)

    def solved(self):
        unsolved_sections = [section for i, section in enumerate(self.sections) if not section.solved()]
        return len(unsolved_sections) == 0

class squareList(object):
    def __init__(self, sudocooldata, by="row"):
        self.squares = []

        if by == "row":
            for i, val in enumerate(sudocooldata.split(',')):
                self.squares.append(square(row=math.floor(i/9), col=i%9, value=val))
        elif by == "section":
            sudocooldata_values = sudocooldata.split(',')
            for section in range(9):
                start_index = section * 9
                end_index = start_index + 9
                sudocooldata_section = sudocooldata_values[start_index:end_index]

                for i, val in enumerate(sudocooldata_section):
                    row = math.floor(i / 3) + 3 * math.floor(section / 3)
                    col = (i % 3) + 3 * (section % 3)

                    self.squares.append(square(row=row, col=col, value=val))

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

class board(object):
    def __init__(self, sudocooldata, by="row"):
        self.squareList = squareList(sudocooldata, by)
        self.rowList = rowList()
        self.colList = colList()
        self.sectionList = sectionList()

    # has the board been solved?
    def solved(self):
        return self.rowList.solved() and self.colList.solved() and self.sectionList.solved()

    # is the board in an inconsistent state, i.e. are there any squares with no possibilities left that aren't solved?
    def inconsistent(self):
        unsolved_squares = [square for i, square in enumerate(self.squareList.squares) if not square.solved and len(square.possibilities) == 0]
        return len(unsolved_squares) > 0

    def solveSquare(self, square, possibility):
        self.rowList.removePossibility(square.row, possibility)
        self.colList.removePossibility(square.col, possibility)
        self.sectionList.removePossibility(square.section, possibility)
        self.squareList.solveAndRemovePossibility(square.row, square.col, square.section, possibility)

    def setupBoard(self):
        for square in self.squareList.squares:
            if square.solved:
                self.rowList.removePossibility(square.row, square.value)
                self.colList.removePossibility(square.col, square.value)
                self.sectionList.removePossibility(square.section, square.value)
                self.squareList.removePossibility(square.row, square.col, square.section, square.value)

    # If a cell has only one possibility, solve that cell
    def singleCandidate(self):
        found = False
        for square in self.squareList.squares:
            if not square.solved and len(square.possibilities) == 1:
                found = True
                self.solveSquare(square, square.possibilities[0])
        return found

    # For each possibility in each row/col/section, if there is only one cell in that row/col/section containing that possibility, solve that cell
    def singlePosition(self):
        found = False
        for row in self.rowList.rows:
            for possibility in row.possibilities:
                squares = [square for i, square in enumerate(self.squareList.squares) if square.row == row.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    self.solveSquare(squares[0], possibility)
        for col in self.colList.cols:
            for possibility in col.possibilities:
                squares = [square for i, square in enumerate(self.squareList.squares) if square.col == col.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    self.solveSquare(squares[0], possibility)
        for section in self.sectionList.sections:
            for possibility in section.possibilities:
                squares = [square for i, square in enumerate(self.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    self.solveSquare(squares[0], possibility)
        return found

    # For each possibility in each section, look at all cells in that section containing that possibility
    # If all such cells fall on a single row or column, that row or column in that section must contain that possibility
    # Therefore, we can remove that possibility from cells in the same row or column in other sections
    def candidateLine(self):
        found = False
        for section in self.sectionList.sections:
            for possibility in section.possibilities:
                rows = set([square.row for i, square in enumerate(self.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                if len(rows) == 1:
                    for remove_square in [square for i, square in enumerate(self.squareList.squares) if square.section != section.index and square.row in rows and square.hasPossibility(possibility)]:
                        found = True
                        remove_square.removePossibility(possibility)
                cols = set([square.col for i, square in enumerate(self.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                if len(cols) == 1:
                    for remove_square in [square for i, square in enumerate(self.squareList.squares) if square.section != section.index and square.col in cols and square.hasPossibility(possibility)]:
                        found = True
                        remove_square.removePossibility(possibility)
        return found

    # For each pair of sections in the same section-row or section-col, look at each possibility in turn that they have in common
    # Look for a possibility that occurs in exactly two rows (for a section-row) or cols (for a section-col), and the same two rows/cols in both sections
    # If such a possibility exists, it must occur in those two rows/cols in those two sections
    # Therefore, remove it from those two rows/cols in the third section in that section-row/col
    def doublePair(self):
        found = False
        for section in self.sectionList.sections:
            for test_section in [s for i, s in enumerate(self.sectionList.sections) if s.rowIndex == section.rowIndex and s.colIndex != section.colIndex]:
                cols = [section.colIndex, test_section.colIndex]
                for possibility in section.possibilities:
                    s_rows = set([square.row for i, square in enumerate(self.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                    ts_rows = set([square.row for i, square in enumerate(self.squareList.squares) if square.section == test_section.index and square.hasPossibility(possibility)])
                    if len(s_rows) == 2 and s_rows == ts_rows:
                        for remove_sections in [s for i, s in enumerate(self.sectionList.sections) if s.rowIndex == section.rowIndex and not s.colIndex in cols]:
                            for remove_squares in [s for i, s in enumerate(self.squareList.squares) if s.section == remove_sections.index and s.row in s_rows and s.hasPossibility(possibility)]:
                                found = True
                                remove_squares.removePossibility(possibility)
            for test_section in [s for i, s in enumerate(self.sectionList.sections) if s.colIndex == section.colIndex and s.rowIndex != section.rowIndex]:
                rows = [section.rowIndex, test_section.rowIndex]
                for possibility in section.possibilities:
                    s_cols = set([square.col for i, square in enumerate(self.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)])
                    ts_cols = set([square.col for i, square in enumerate(self.squareList.squares) if square.section == test_section.index and square.hasPossibility(possibility)])
                    if len(s_cols) == 2 and s_cols == ts_cols:
                        for remove_sections in [s for i, s in enumerate(self.sectionList.sections) if s.colIndex == section.colIndex and not s.rowIndex in rows]:
                            for remove_squares in [s for i, s in enumerate(self.squareList.squares) if s.section == remove_sections.index and s.col in s_cols and s.hasPossibility(possibility)]:
                                found = True
                                remove_squares.removePossibility(possibility)
        return found

    # For each row/col/section, look through all squares in that row/col/section
    # If any N squares have exactly the same N possibilities, only those N squares in that row/col/section can contain those N possibilities
    # For example if two square share the same two possibilities, those two squares must contain those two possibilities, and no other squares in that row can have either possibility
    # Therefore, remove those N possibilities from all other squares in that row/col/section
    def nakedTuples(self):
        found = False
        for row in self.rowList.rows:
            for test_square in [square for i, square in enumerate(self.squareList.squares) if square.row == row.index and not square.solved]:
                match_squares = [square for i, square in enumerate(self.squareList.squares) if square.row == row.index and not square.solved and square.possibilities == test_square.possibilities]
                if len(match_squares) == len(test_square.possibilities):
                    for remove_square in [square for i, square in enumerate(self.squareList.squares) if square.row == row.index and not square.solved and square.hasPartialIntersect(test_square.possibilities)]:
                        found = True
                        remove_square.removePossibilities(test_square.possibilities)
        for col in self.colList.cols:
            for test_square in [square for i, square in enumerate(self.squareList.squares) if square.col == col.index and not square.solved]:
                match_squares = [square for i, square in enumerate(self.squareList.squares) if square.col == col.index and not square.solved and square.possibilities == test_square.possibilities]
                if len(match_squares) == len(test_square.possibilities):
                    for remove_square in [square for i, square in enumerate(self.squareList.squares) if square.col == col.index and not square.solved and square.hasPartialIntersect(test_square.possibilities)]:
                        found = True
                        remove_square.removePossibilities(test_square.possibilities)
        for section in self.sectionList.sections:
            for test_square in [square for i, square in enumerate(self.squareList.squares) if square.section == section.index and not square.solved]:
                match_squares = [square for i, square in enumerate(self.squareList.squares) if square.section == section.index and not square.solved and square.possibilities == test_square.possibilities]
                if len(match_squares) == len(test_square.possibilities):
                    for remove_square in [square for i, square in enumerate(self.squareList.squares) if square.section == section.index and not square.solved and square.hasPartialIntersect(test_square.possibilities)]:
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
        unsolved_squares = [square for i, square in enumerate(self.squareList.squares) if not square.solved]
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

    def solveBoard(self):
        self.solveRound()

        if self.solved():
            return True
        elif self.inconsistent():
            return False

        result = True
        while result:
            result = self.guess()

    def __str__(self):
        ret_str = "\nRows:\n\n"
        ret_str += "\n".join(str(r) for r in self.rowList.rows)
        ret_str += "\n\nCols:\n\n"
        ret_str += "\n".join(str(c) for c in self.colList.cols)
        ret_str += "\n\nSections:\n\n"
        ret_str += "\n".join(str(s) for s in self.sectionList.sections)
        ret_str += "\n\nSquares:\n\n"
        ret_str += "\n".join(str(s) for s in self.squareList.squares)
        return ret_str

    def printBoard(self):
        return ",".join(str(s.value) for s in self.squareList.squares)

    def printBoardBySection(self):
        board_sections = []
        for section in self.sectionList.sections:
            section_squares = [
                square for square in self.squareList.squares
                if square.section == section.index]

            board_sections.append(",".join(str(square.value) for square in section_squares))

        return ",".join(board_section for board_section in board_sections)
