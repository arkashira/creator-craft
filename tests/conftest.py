import pytest

@pytest.fixture(autouse=True)
def add_src_to_path():
    import sys
    sys.path.insert(0, 'src')
