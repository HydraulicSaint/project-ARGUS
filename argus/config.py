import os
from dotenv import load_dotenv

load_dotenv()

# FIRMS API key is read from the environment variable ``FIRMS_API_KEY``.
# Users should create a `.env` file or export the variable before running.
MAP_KEY = os.getenv("FIRMS_API_KEY", "")
