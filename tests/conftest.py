import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
# Must be set before importing the app (the app reads MODEL_DIR when it is imported).
os.environ.setdefault("MODEL_DIR", str(ROOT / "model"))

from src.app import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    """One TestClient for the whole session; `with` runs the startup that loads the model."""
    with TestClient(app) as test_client:
        yield test_client
