import os

"""Configuration constants for ARGUS."""

MAP_KEY = os.getenv("ARGUS_MAP_KEY")
if not MAP_KEY:
    raise ValueError(
        "MAP_KEY not set. Please define the ARGUS_MAP_KEY environment variable.")
