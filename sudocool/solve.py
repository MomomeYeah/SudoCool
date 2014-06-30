import math

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
            self.possibilities = [1,2,3,4,5,6,7,8,9]

    def __str__(self):
        ret_str = "Row: "+str(self.row)+", Col: "+str(self.col)+", Section: "+str(self.section)
        ret_str += ", Value: "+str(self.value)+", Solved: "+str(self.solved)+", "
        if not self.solved:
            for i in self.possibilities: ret_str += str(i)+","
        return ret_str

    def removePossibility(self, possibility):
        if not self.solved and possibility in self.possibilities:
            self.possibilities.remove(possibility)

    def solve(self, possibility):
        self.solved = True
        self.value = possibility
        self.possibilities = None

    def hasPossibility(self, possibility):
        return self.solved == False and possibility in self.possibilities

class rowColOrSection(object):
    def __init__(self, index):
        self.index = index
        self.possibilities = [1,2,3,4,5,6,7,8,9]

    def __str__(self):
        ret_str = "Index: "+str(self.index)+", Possibilities: "
        for i in self.possibilities: ret_str += str(i)+","
        return ret_str

    def __eq__(self, index):
        return self.index == index

    def removePossibility(self, possibility):
        if possibility in self.possibilities:
            self.possibilities.remove(possibility)

class rowList(object):
    def __init__(self):
        self.rows = []
        for i in range(9):
            self.rows.append(rowColOrSection(i))

    def removePossibility(self, index, possibility):
        r = self.rows[self.rows.index(index)]
        r.removePossibility(possibility)

class colList(object):
    def __init__(self):
        self.cols = []
        for i in range(9):
            self.cols.append(rowColOrSection(i))

    def removePossibility(self, index, possibility):
        c = self.cols[self.cols.index(index)]
        c.removePossibility(possibility)

class sectionList(object):
    def __init__(self):
        self.sections = []
        for i in range(9):
            self.sections.append(rowColOrSection(i))

    def removePossibility(self, index, possibility):
        s = self.sections[self.sections.index(index)]
        s.removePossibility(possibility)

class squareList(object):
    def __init__(self, sudocooldata):
        self.squares = []
        i = 0
        for val in sudocooldata.split(','):
            self.squares.append(square(math.floor(i/9), i%9, val))
            i += 1
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
    def __init__(self, sudocooldata):
        self.squareList = squareList(sudocooldata)
        self.rowList = rowList()
        self.colList = colList()
        self.sectionList = sectionList()

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
                self.rowList.removePossibility(square.row, square.possibilities[0])
                self.colList.removePossibility(square.col, square.possibilities[0])
                self.sectionList.removePossibility(square.section, square.possibilities[0])
                self.squareList.solveAndRemovePossibility(square.row, square.col, square.section, square.possibilities[0])
        return found

    # For each possibility in each row/col/section, if there is only one cell in that row/col/section containing that possibility, solve that cell
    def singlePosition(self):
        found = False
        for row in self.rowList.rows:
            for possibility in row.possibilities:
                squares = [square for i, square in enumerate(self.squareList.squares) if square.row == row.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    square = squares[0]
                    row.removePossibility(possibility)
                    self.squareList.solveAndRemovePossibility(square.row, square.col, square.section, possibility)
                    self.colList.removePossibility(square.col, possibility)
                    self.sectionList.removePossibility(square.section, possibility)
        for col in self.colList.cols:
            for possibility in col.possibilities:
                squares = [square for i, square in enumerate(self.squareList.squares) if square.col == col.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    square = squares[0]
                    col.removePossibility(possibility)
                    self.squareList.solveAndRemovePossibility(square.row, square.col, square.section, possibility)
                    self.rowList.removePossibility(square.row, possibility)
                    self.sectionList.removePossibility(square.section, possibility)
        for section in self.sectionList.sections:
            for possibility in section.possibilities:
                squares = [square for i, square in enumerate(self.squareList.squares) if square.section == section.index and square.hasPossibility(possibility)]
                if len(squares) == 1:
                    found = True
                    square = squares[0]
                    section.removePossibility(possibility)
                    self.squareList.solveAndRemovePossibility(square.row, square.col, square.section, possibility)
                    self.rowList.removePossibility(square.row, possibility)
                    self.colList.removePossibility(square.col, possibility)
        return found

    # For each possibility in each section, look at all cells in that section containing that possibility
    # If all such cells fall on a single row or column, that row or column in that section must contain that possibility
    # Therefore, we can remove that possibility from cells in the same row or column in other sections 
    def candidateLine(self):
        found = False
        for section in self.sectionList.sections:
            for possibility in section.possibilities:
                rows = []
                for square in self.squareList.squares:
                    if square.section == section.index and square.hasPossibility(possibility):
                        if square.row not in rows:
                            rows.append(square.row)
                if len(rows) == 1:
                    for square in self.squareList.squares:
                        if square.row == rows[0] and square.section != section.index and square.hasPossibility(possibility):
                            found = True
                            square.removePossibility(possibility)
                cols = []
                for square in self.squareList.squares:
                    if square.section == section.index and square.hasPossibility(possibility):
                        if square.col not in cols:
                            cols.append(square.col)
                if len(cols) == 1:
                    for square in self.squareList.squares:
                        if square.col == cols[0] and square.section != section.index and square.hasPossibility(possibility):
                            found = True
                            square.removePossibility(possibility)
        return found

    # For each row/col/section, look through all squares in that row/col/section
    # If any two have exactly the same two possibilities, only those two squares in that row/col/section can contain those two possibilities
    # Therefore, remove those two possibilities from all other squares in that row/col/section
    def nakedPairs(self):
        found = False
        for row in self.rowList.rows:
            possibilities = None
            for square in self.squareList.squares:
                if square.row == row.index and square.solved == False and len(square.possibilities) == 2:
                    if possibilities == None:
                        possibilities = square.possibilities
                    elif possibilities == square.possibilities:
                        for square_remove in self.squareList.squares:
                            if square_remove.row == row.index and square_remove.solved == False and not square_remove.possibilities == possibilities:
                                found = True
                                for possibility in possibilities:
                                    square_remove.removePossibility(possibility)
        for col in self.colList.cols:
            possibilities = None
            for square in self.squareList.squares:
                if square.col == col.index and square.solved == False and len(square.possibilities) == 2:
                    if possibilities == None:
                        possibilities = square.possibilities
                    elif possibilities == square.possibilities:
                        for square_remove in self.squareList.squares:
                            if square_remove.col == col.index and square_remove.solved == False and not square_remove.possibilities == possibilities:
                                found = True
                                for possibility in possibilities:
                                    square_remove.removePossibility(possibility)
        for section in self.sectionList.sections:
            possibilities = None
            for square in self.squareList.squares:
                if square.section == section.index and square.solved == False and len(square.possibilities) == 2:
                    if possibilities == None:
                        possibilities = square.possibilities
                    elif possibilities == square.possibilities:
                        for square_remove in self.squareList.squares:
                            if square_remove.section == section.index and square_remove.solved == False and not square_remove.possibilities == possibilities:
                                found = True
                                for possibility in possibilities:
                                    square_remove.removePossibility(possibility)
        return found

    def solveBoard(self):
        found = True
        while found:
            found = False
            found = self.singleCandidate()
            if not found:
                found = self.singlePosition()
            if not found:
                found = self.candidateLine()
            if not found:
                found = self.nakedPairs()
            
    def __str__(self):
        ret_str = "Rows:\n"
        for r in self.rowList.rows:
            ret_str += str(r)+"\n"
        ret_str += "Cols:\n"
        for c in self.colList.cols:
            ret_str += str(c)+"\n"
        ret_str += "Sections:\n"
        for s in self.sectionList.sections:
            ret_str += str(s)+"\n"
        ret_str += "Squares:\n"
        for s in self.squareList.squares:
            ret_str += str(s)+"\n"
        return ret_str

    def printBoard(self):
        ret_str = ""
        for s in self.squareList.squares:
            ret_str += str(s.value)+","
        return ret_str
