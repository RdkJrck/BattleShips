import pytest
from board import BoardError, Board,BOARD_SIZE, SHIP_SYMBOL, WATER_SYMBOL
from ships import scout_ship

def test_in_bounds():
    board = Board()
    assert board.in_bounds(0,0) == True
    assert board.in_bounds(BOARD_SIZE - 1, BOARD_SIZE - 1) == True
    assert board.in_bounds(BOARD_SIZE, 0) == False
    assert board.in_bounds( -1, BOARD_SIZE - 1) == False

def test_place_ship():
    board = Board()
    board.place_ship(1, scout_ship(), 3, 4 ) == True
    assert board.grid[(3,4)] == 1
    assert board.grid[(3,5)] == 1
    assert board.symbol(3,4) == SHIP_SYMBOL
    assert board.symbol(3,6) == WATER_SYMBOL


def test_ship_out_bounds():
    board = Board()
    with pytest.raises(BoardError):
        board.place_ship(1, scout_ship(),3,-1)
    with pytest.raises(BoardError):
        board.place_ship(1, scout_ship(),BOARD_SIZE+2,5)
    pass


def test_place_ship_collision():
    board = Board()
    board.place_ship(1,scout_ship(), 3, 4 )
    with pytest.raises(BoardError):
        board.place_ship(1,scout_ship(), 3, 4, horizontal = True )
    pass