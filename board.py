from ships import Ship
BOARD_SIZE = 4096 # 1024
GRID_SIZE_M = 5
EMPTY_ID = 0
FOV = 20
SHIP_SYMBOL = "0"
HIT_SYMBOL = "X"
WATER_SYMBOL = "+"
GRID_ZONE = "50R"
SQUARE_ID = "MM"

class BoardError(Exception):
    pass

class Board:
    def __init__(self, size: int = BOARD_SIZE):
        self.size = size
        self.grid = {}
        self.terrain = {}
        self.ships = {}

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <=y < self.size

    def symbol(self, x: int, y: int) -> str:
        val = self.grid.get((x,y), EMPTY_ID)
        if val > 0:
            return SHIP_SYMBOL
        if val < 0:
            return HIT_SYMBOL
        else:
             return WATER_SYMBOL

    def place_ship(self, ship_id: int, ship:Ship, x: int, y: int, horizontal: bool = False) -> None:
        w,l = (ship.length, ship.width) if horizontal else (ship.width, ship.length)
        coords = []
        for cx in range(x, x + w ):
            for cy in range(y, y + l):
                coords.append((cx, cy))
        for cx, cy in coords:
            if not self.in_bounds(cx, cy):
                raise BoardError(f"Out of bounds x:{cx} y:{cy}")
            if (cx, cy) in self.grid:
                raise BoardError(f"Collision on x:{cx} y:{cy}")
        for cx, cy in coords:
            self.grid[(cx,cy)] = ship_id
        self.ships[ship_id] = ship

    def fire(self, x: int, y: int) -> bool:
        if not self.in_bounds(x, y):
            raise BoardError(f"Out of bounds x:{x} y:{y}")
        val = self.grid.get((x, y), EMPTY_ID)
        if val > 0:
            self.grid[(x, y)] = -val
            return True
        return False

    def render(self, x0: int = 0, y0: int = 0, fov: int = FOV) -> str:
        rows = []
        header = "    " + "  ".join(str(x % 10) for x in range(x0, x0 + fov ))
        rows.append(header)
        for y in range(y0, y0 + fov):
            row = "  ".join (self.symbol(x,y) for x in range(x0, x0 + fov))
            rows.append(f"{y:03d} " + row)
        return "\n".join(rows)


                


