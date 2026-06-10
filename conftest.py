"""Root conftest — adds game/ to sys.path so tests import systems.* and api."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "game"))
