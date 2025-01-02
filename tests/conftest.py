import pytest
from pathlib import Path
import sys

# Add src to Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

@pytest.fixture
def test_data_dir():
    return Path(__file__).parent / 'data'
