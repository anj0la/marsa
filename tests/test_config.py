import pytest
from pathlib import Path
from marsa.src.marsa.config import (
    load_aspect_config,
    AspectConfig,
    check_file_extension
)

# ---------- Regular Tests ----------

# NEED TO REWRITE TEST CASES

# ---------- Edge Case Tests ----------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_aspect_config('examples/nonexistent.yaml')

def test_invalid_extension_raises():
    # Arrange
    invalid_file = Path('examples/unsupported.csv')
    
    # Act
    invalid_file.write_text('dummy content')  # create a dummy CSV file temporarily
    
    # Assert
    with pytest.raises(NameError):
        load_aspect_config(str(invalid_file))

    invalid_file.unlink()  # cleanup

def test_check_file_extension_logic():
    assert check_file_extension('example.json', ['.json']) is True
    assert check_file_extension('example.yml', ['.yaml', '.yml']) is True
    assert check_file_extension('example.txt', ['.json']) is False
