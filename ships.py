from dataclasses import dataclass

@dataclass(frozen=True)
class Ship:
    kind: str 
    width: int
    length: int
    mobility: int
    move_cost: int
    spot_range: int
    firing_range: int
    damage_radius: int

def scout_ship() -> Ship:
    return Ship(
        kind = "Scout",
        width = 1,
        length = 2,
        mobility = 5,
        move_cost = 1,
        spot_range = 32,
        firing_range = 12,
        damage_radius = 1,
    )

def frigate_ship() -> Ship:
    return Ship(
        kind = "Frigate",
        width = 2,
        length = 3,
        mobility = 3,
        move_cost = 3,
        spot_range = 30,
        firing_range = 16,
        damage_radius = 2,
    )

def destroyer_ship() -> Ship:
    return Ship(
        kind = "Destroyer",
        width = 3,
        length = 5,
        mobility = 1,
        move_cost = 5,
        spot_range = 28,
        firing_range = 32,
        damage_radius = 3,
    )