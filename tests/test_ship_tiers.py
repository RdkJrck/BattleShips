from ships import scout_ship, frigate_ship, destroyer_ship

def test_ship_tiers():
    scout = scout_ship()
    frigate = frigate_ship()
    destroyer = destroyer_ship()
    assert scout.mobility > frigate.mobility > destroyer.mobility
    assert scout.damage_radius < frigate.damage_radius < destroyer.damage_radius
    