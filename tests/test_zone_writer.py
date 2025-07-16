from argus.scanner.zone_writer import write_zone
import json
import os

def test_write_zone(tmp_path):
    path = write_zone("Test Zone", 0, 1, 2, 3, directory=tmp_path)
    assert os.path.exists(path)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data["name"] == "Test Zone"
    assert data["lat_min"] == 0
