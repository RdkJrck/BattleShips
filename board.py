BOARD_SIZE = 256

class Board:
    def __init__(self):
        pass

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x <= BOARD_SIZE and 0 <= y <= BOARD_SIZE

