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

class row(object):
    def __init__(self, index):
        self.index = index
        self.possibilities = [1,2,3,4,5,6,7,8,9]

    def __str__(self):
        ret_str = "Index: "+str(self.index)+", Possibilities: "
        for i in self.possibilities: ret_str += str(i)+","
        return ret_str

    def __eq__(self, index):
        return self.index == index

class col(object):
    def __init__(self, index):
        self.index = index
        self.possibilities = [1,2,3,4,5,6,7,8,9]

    def __str__(self):
        ret_str = "Index: "+str(self.index)+", Possibilities: "
        for i in self.possibilities: ret_str += str(i)+","
        return ret_str

    def __eq__(self, index):
        return self.index == index

class section(object):
    def __init__(self, index):
        self.index = index
        self.possibilities = [1,2,3,4,5,6,7,8,9]

    def __str__(self):
        ret_str = "Index: "+str(self.index)+", Possibilities: "
        for i in self.possibilities: ret_str += str(i)+","
        return ret_str

    def __eq__(self, index):
        return self.index == index

class board(object):
    def __init__(self, sudocooldata):
        self.squares = []
        self.rows = []
        self.cols = []
        self.sections = []
        for i in range(9):
            self.rows.append(row(i))
            self.cols.append(col(i))
            self.sections.append(section(i))
        i = 0
        for val in sudocooldata.split(','):
            self.squares.append(square(math.floor(i/9), i%9, val))
            i += 1

    def setupBoard(self):
        for square in self.squares:
            if square.solved:
                r = self.rows[self.rows.index(square.row)]
                if square.value in r.possibilities: r.possibilities.remove(square.value)

                c = self.cols[self.cols.index(square.col)]
                if square.value in c.possibilities: c.possibilities.remove(square.value)

                s = self.sections[self.sections.index(square.section)]
                if square.value in s.possibilities: s.possibilities.remove(square.value)

                for square_remove in self.squares:
                    if square_remove.row == square.row or square_remove.col == square.col or square_remove.section == square.section:
                        if not square_remove.solved and square.value in square_remove.possibilities:
                            square_remove.possibilities.remove(square.value)

    def checkRows(self):
        found = False
        for row in self.rows:
            for possibility in row.possibilities:
                count = 0
                col = 0
                section = 0
                for square in self.squares:
                    if square.row == row.index and square.solved == False and possibility in square.possibilities:
                        count += 1
                        col = square.col
                        section = square.section
                if count == 1:
                    found = True
                    row.possibilities.remove(possibility)
                    for sq in self.squares:
                        if sq.row == row.index and sq.col == col:
                            sq.solved = True
                            sq.value = possibility
                            sq.possibilities = None
                        elif not sq.solved:
                            if sq.row == row.index and not sq.col == col and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                            elif not sq.row == row.index and sq.col == col and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                            elif not sq.row == row.index and not sq.col == col and sq.section == section and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                    for col_remove in self.cols:
                        if col_remove.index == col:
                            col_remove.possibilities.remove(possibility)
                    for section_remove in self.sections:
                        if section_remove.index == section:
                            section_remove.possibilities.remove(possibility)
        return found

    def checkCols(self):
        found = False
        for col in self.cols:
            for possibility in col.possibilities:
                count = 0
                row = 0
                section = 0
                for square in self.squares:
                    if square.col == col.index and square.solved == False and possibility in square.possibilities:
                        count += 1
                        row = square.row
                        section = square.section
                if count == 1:
                    found = True
                    col.possibilities.remove(possibility)
                    for sq in self.squares:
                        if sq.row == row and sq.col == col.index:
                            sq.solved = True
                            sq.value = possibility
                            sq.possibilities = None
                        elif not sq.solved:
                            if sq.row == row and not sq.col == col.index and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                            elif not sq.row == row and sq.col == col.index and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                            elif not sq.row == row and not sq.col == col.index and sq.section == section and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                    for row_remove in self.rows:
                        if row_remove.index == row:
                            row_remove.possibilities.remove(possibility)
                    for section_remove in self.sections:
                        if section_remove.index == section:
                            section_remove.possibilities.remove(possibility)
        return found

    def checkSections(self):
        found = False
        for section in self.sections:
            for possibility in section.possibilities:
                count = 0
                row = 0
                col = 0
                for square in self.squares:
                    if square.section == section.index and square.solved == False and possibility in square.possibilities:
                        count += 1
                        row = square.row
                        col = square.col
                if count == 1:
                    found = True
                    section.possibilities.remove(possibility)
                    for sq in self.squares:
                        if sq.row == row and sq.col == col:
                            sq.solved = True
                            sq.value = possibility
                            sq.possibilities = None
                        elif not sq.solved:
                            if sq.row == row and not sq.col == col and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                            elif not sq.row == row and sq.col == col and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                            elif not sq.row == row and not sq.col == col and sq.section == section.index and possibility in sq.possibilities:
                                sq.possibilities.remove(possibility)
                    for row_remove in self.rows:
                        if row_remove.index == row:
                            row_remove.possibilities.remove(possibility)
                    for col_remove in self.cols:
                        if col_remove.index == col:
                            col_remove.possibilities.remove(possibility)
        return found

    def solveBoard(self):
        found = True
        while found:
            found = False
            found = self.checkRows()
            if not found:
                found = self.checkCols()
            if not found:
                found = self.checkSections()
            
    def __str__(self):
        ret_str = "Rows:\n"
        for r in self.rows:
            ret_str += str(r)+"\n"
        ret_str += "Cols:\n"
        for c in self.cols:
            ret_str += str(c)+"\n"
        ret_str += "Sections:\n"
        for s in self.sections:
            ret_str += str(s)+"\n"
        ret_str += "Squares:\n"
        for s in self.squares:
            ret_str += str(s)+"\n"
        return ret_str

    def printBoard(self):
        ret_str = ""
        for s in self.squares:
            ret_str += str(s.value)+","
        return ret_str
