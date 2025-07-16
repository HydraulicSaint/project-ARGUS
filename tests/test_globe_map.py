from argus.visualize.globe_map import build_globe


def test_build_globe_creates_file(tmp_path):
    log = [{
        "name": "tile_0_0",
        "lat_min": 0,
        "lat_max": 1,
        "lon_min": 0,
        "lon_max": 1,
        "status": "heat",
        "hits": 1,
        "timestamp": "now"
    }]
    out = tmp_path / "globe.html"
    build_globe(log, output=str(out))
    assert out.exists()

