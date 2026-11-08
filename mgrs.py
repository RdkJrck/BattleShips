from board import GRID_ZONE, SQUARE_ID
class MGRS_Error(Exception):
    pass

def parse_mgrs(coords: str) -> tuple[int, int]:
    #Zkontroluji format
    if not isinstance(coords, str) or not coords.isdigit() or len(coords) != 10:
        raise MGRS_Error(f"Coordinates are invald!: {coords}")
    #Zapis hodnoty
    e_cord = int(coords[0:5]) 
    n_cord = int(coords[5:10])
    
    return (e_cord,n_cord)

def format_mgrs(x:int , y: int ) -> str:
    if x < 0 or y < 0:
        raise MGRS_Error(f"Coordinates are out of range!: {x}, {y}")
    return f"{x:05d}{y:05d}"
