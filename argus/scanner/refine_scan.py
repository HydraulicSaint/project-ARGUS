from argus.scanner.coarse_grid import generate_grid


def refine_scan(scan_log, step=1):
    """Return a finer grid for all heat detections in a scan log."""
    refined = []
    for entry in scan_log:
        if entry.get("status") == "heat":
            refined.extend(
                generate_grid(
                    step=step,
                    lat_range=(entry["lat_min"], entry["lat_max"]),
                    lon_range=(entry["lon_min"], entry["lon_max"]),
                )
            )
    return refined
