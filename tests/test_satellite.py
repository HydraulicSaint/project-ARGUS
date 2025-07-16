from argus.utils.satellite import fetch_satellite_image, classify_thermal_anomaly
from unittest.mock import patch, MagicMock
from pathlib import Path


def test_fetch_satellite_image(tmp_path):
    dummy_data = b"imagebytes"
    mock_resp = MagicMock()
    mock_resp.read.return_value = dummy_data
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = False
    with patch("urllib.request.urlopen", return_value=mock_resp):
        out_file = tmp_path / "img.png"
        path = fetch_satellite_image(0, 0, output=str(out_file))
        assert Path(path).exists()
        assert out_file.read_bytes() == dummy_data


def test_classify_thermal_anomaly(tmp_path):
    small = tmp_path / "small.png"
    small.write_bytes(b"x" * 100)
    assert classify_thermal_anomaly(str(small), threshold=200) == "no anomaly"

    large = tmp_path / "large.png"
    large.write_bytes(b"x" * 1000)
    assert classify_thermal_anomaly(str(large), threshold=200) == "hot spot"
