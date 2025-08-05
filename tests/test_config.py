import pytest
from pathlib import Path
from marsa.config import AspectConfig, load_aspect_config, check_file_extension
from tests.constants import ASPECT_CONFIG

# ---------- Regular Tests ----------

def test_load_yaml_aspects_only_example():
    # Arrange
    path = 'tests/data/test_aspect_only.yaml'

    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert config.category_to_terms is None
    
    # Assert - Expected values == Actual values
    assert len(config.aspect_terms) == len(ASPECT_CONFIG.aspect_terms)
    for i in range(len(config.aspect_terms)):
        assert config.aspect_terms[i] == ASPECT_CONFIG.aspect_terms[i]
    
def test_load_yaml_aspects_with_categories_example():
    # Arrange
    path = 'tests/data/test_aspect.yaml'

    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert config.category_to_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert isinstance(config.category_to_terms, dict)
    assert all(isinstance(v, list) for v in config.category_to_terms.values())
    
    # Expected values == Actual values
    assert len(config.aspect_terms) == len(ASPECT_CONFIG.aspect_terms)
    assert len(config.category_to_terms) == len(ASPECT_CONFIG.category_to_terms)
    for i in range(len(config.aspect_terms)):
        assert config.aspect_terms[i] == ASPECT_CONFIG.aspect_terms[i]
    for key in config.category_to_terms:
        assert key in ASPECT_CONFIG.category_to_terms
        assert config.category_to_terms[key] == ASPECT_CONFIG.category_to_terms[key]

def test_load_json_aspects_only_example():
    # Arrange
    path = 'tests/data/test_aspect_only.json'
    
    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert config.category_to_terms is None
    
    # Expected values == Actual values
    assert len(config.aspect_terms) == len(ASPECT_CONFIG.aspect_terms)
    for i in range(len(config.aspect_terms)):
        assert config.aspect_terms[i] == ASPECT_CONFIG.aspect_terms[i]
    
def test_load_json_with_categories_example():
    # Arrange
    path = 'tests/data/test_aspect.json'
    
    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert config.category_to_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert isinstance(config.category_to_terms, dict)
    assert all(isinstance(v, list) for v in config.category_to_terms.values())
    
    # Expected values == Actual values
    assert len(config.aspect_terms) == len(ASPECT_CONFIG.aspect_terms)
    assert len(config.category_to_terms) == len(ASPECT_CONFIG.category_to_terms)
    for i in range(len(config.aspect_terms)):
        assert config.aspect_terms[i] == ASPECT_CONFIG.aspect_terms[i]
    for key in config.category_to_terms:
        assert key in ASPECT_CONFIG.category_to_terms
        assert config.category_to_terms[key] == ASPECT_CONFIG.category_to_terms[key]

# ---------- Edge Case Tests ----------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_aspect_config('tests/data/nonexistent.yaml')

def test_invalid_extension_raises():
    # Arrange
    invalid_file = Path('tests/data/unsupported.csv')
    
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
