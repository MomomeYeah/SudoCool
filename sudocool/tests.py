from django.test import TestCase
from sudocool.models import SudocoolBoard
from sudocool.solve import *

def create_sudocoolboard(sudocooldata):
    """
    Creates a SudocoolBoard with the given sudocooldata
    """
    return SudocoolBoard.objects.create_sudocoolboard(sudocooldata)

def create_board(SudocoolBoard):
    """
    Creates a board object from a given SudocoolBoard
    """
    return board(SudocoolBoard.sudocoolData)

def create_board_from_data(sudocooldata):
    """
    Creates a board object from given sudocooldata
    """
    return create_board(create_sudocoolboard(sudocooldata))

class BoardSolveTests(TestCase):
    def test_basic_board_one(self):
        """
        Check solution is correct
        """
        board = ",,,5,,,,2,,,4,1,,6,7,9,,,2,,9,,8,,7,,6,7,3,6,,,2,,,4,5,,,,,,,,8,4,,,3,,,1,6,2,9,,4,,5,,6,,3,,,3,4,2,,8,5,,,7,,,,1,,,"
        solution = "6,8,7,5,9,3,4,2,1,3,4,1,2,6,7,9,8,5,2,5,9,1,8,4,7,3,6,7,3,6,8,1,2,5,9,4,5,1,2,9,4,6,3,7,8,4,9,8,3,7,5,1,6,2,9,2,4,7,5,8,6,1,3,1,6,3,4,2,9,8,5,7,8,7,5,6,3,1,2,4,9,"
        b = create_board_from_data(board)
        b.setupBoard()
        b.solveBoard()
        
        self.assertEqual(b.printBoard(), solution)

    def test_basic_board_two(self):
        """
        Check solution is correct
        """
        board = ",3,4,6,,,,,,5,,,1,,,,4,6,,7,,5,2,,3,,1,,4,9,8,,,,,3,,,6,4,,1,7,,,2,,,,,7,9,8,,9,,5,,3,6,,1,,8,1,,,,5,,,9,,,,,,8,2,7,"
        solution = "1,3,4,6,8,9,5,2,7,5,9,2,1,7,3,8,4,6,6,7,8,5,2,4,3,9,1,7,4,9,8,5,2,1,6,3,3,8,6,4,9,1,7,5,2,2,5,1,3,6,7,9,8,4,9,2,5,7,3,6,4,1,8,8,1,7,2,4,5,6,3,9,4,6,3,9,1,8,2,7,5,"
        b = create_board_from_data(board)
        b.setupBoard()
        b.solveBoard()
        
        self.assertEqual(b.printBoard(), solution)

    def test_medium_board_one(self):
        """
        Check solution is correct
        """
        board = "9,,,,,,,,5,,2,7,,,,4,3,,5,,,4,,3,,,1,,,2,,7,,5,,,8,,,9,,2,,,7,,,6,,8,,9,,,4,,,3,,1,,,6,,3,1,,,,8,9,,6,,,,,,,,2"
        solution = "9,4,3,2,1,7,6,8,5,1,2,7,6,5,8,4,3,9,5,6,8,4,9,3,2,7,1,3,9,2,1,7,6,5,4,8,8,5,4,9,3,2,1,6,7,7,1,6,5,8,4,9,2,3,4,8,9,3,2,1,7,5,6,2,3,1,7,6,5,8,9,4,6,7,5,8,4,9,3,1,2,"
        b = create_board_from_data(board)
        b.setupBoard()
        b.solveBoard()
        
        self.assertEqual(b.printBoard(), solution)

    def test_medium_board_two(self):
        """
        Check solution is correct
        """
        board = ",1,,7,,3,,9,,,,2,1,,9,5,,,8,,,,6,,,,3,6,,5,,,,4,,1,,7,,,,,,5,,9,,8,,,,7,,2,4,,,,1,,,,9,,,9,2,,7,3,,,,5,,8,,6,,1,"
        solution = "5,1,4,7,2,3,6,9,8,3,6,2,1,8,9,5,4,7,8,9,7,5,6,4,1,2,3,6,3,5,9,7,2,4,8,1,2,7,1,4,3,8,9,5,6,9,4,8,6,5,1,7,3,2,4,2,6,3,1,5,8,7,9,1,8,9,2,4,7,3,6,5,7,5,3,8,9,6,2,1,4,"
        b = create_board_from_data(board)
        b.setupBoard()
        b.solveBoard()
        
        self.assertEqual(b.printBoard(), solution)

    def test_hard_board_one(self):
        """
        Check solution is correct
        """
        board = ",,,,6,,3,,,,,,8,,,9,6,,,,,,,,5,,2,1,3,,,,5,,,8,,2,,7,,9,,4,,9,,,2,,,,3,6,4,,2,,,,,,,,9,1,,,7,,,,,,5,,1,,,,"
        solution = "2,8,9,5,6,4,3,7,1,5,1,3,8,7,2,9,6,4,7,4,6,1,9,3,5,8,2,1,3,7,6,4,5,2,9,8,6,2,8,7,3,9,1,4,5,9,5,4,2,8,1,7,3,6,4,7,2,3,5,6,8,1,9,8,9,1,4,2,7,6,5,3,3,6,5,9,1,8,4,2,7,"
        b = create_board_from_data(board)
        b.setupBoard()
        b.solveBoard()
        
        self.assertEqual(b.printBoard(), solution)

    def test_hard_board_two(self):
        """
        Check solution is correct
        """
        board = ",2,5,,,,7,,,,,4,,9,,,,3,,3,,,,6,,,,1,,,,2,,,,8,,,,6,,8,,,,7,,,,3,,,,5,,,,8,,,,6,,3,,,,7,,4,,,,,9,,,,2,5,"
        solution = "8,2,5,3,1,4,7,9,6,6,7,4,2,9,5,8,1,3,9,3,1,7,8,6,5,4,2,1,5,6,4,2,7,9,3,8,2,9,3,6,5,8,1,7,4,7,4,8,9,3,1,6,2,5,5,1,7,8,4,2,3,6,9,3,6,2,5,7,9,4,8,1,4,8,9,1,6,3,2,5,7,"
        b = create_board_from_data(board)
        b.setupBoard()
        b.solveBoard()
        
        self.assertEqual(b.printBoard(), solution)
