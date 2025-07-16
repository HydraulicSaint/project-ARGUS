from argus.scanner.coarse_grid import generate_grid

def test_generate_grid_count():
    tiles = generate_grid(step=10, lat_range=(-20, 20), lon_range=(-20, 20))
    assert len(tiles) == 16
    first = tiles[0]
    assert first['lat_min'] == -20 and first['lon_min'] == -20
