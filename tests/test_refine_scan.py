from argus.scanner.refine_scan import refine_scan


def test_refine_scan_returns_subtiles():
    log = [{
        'name': 'tile_0_0',
        'lat_min': 0,
        'lat_max': 5,
        'lon_min': 0,
        'lon_max': 5,
        'status': 'heat'
    }]
    refined = refine_scan(log, step=1)
    # 5x5 grid in 1-degree steps -> 25 tiles
    assert len(refined) == 25
