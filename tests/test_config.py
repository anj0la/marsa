import pytest
from pathlib import Path
from marsa.src.marsa.config import AspectConfig, load_aspect_config, check_file_extension

# ---------- Regular Tests ----------

def test_load_yaml_aspects_only_example():
    # Arrange
    path = 'test/data/test_aspect_only.yaml'

    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert config.category_to_terms is None
    
def test_load_yaml_aspects_with_categories_example():
    # Arrange
    path = 'test/data/test_aspect.yaml'

    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert config.category_to_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert isinstance(config.category_to_terms, dict)
    assert all(isinstance(v, list) for v in config.category_to_terms.values())

def test_load_json_aspects_only_example():
    # Arrange
    path = 'test/data/test_aspect_only.json'
    
    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert config.category_to_terms is None

def test_load_json_with_categories_example():
    # Arrange
    path = 'test/data/test_aspect.json'
    
    # Act
    config = load_aspect_config(path)

    # Assert
    assert isinstance(config, AspectConfig)
    assert config.aspect_terms is not None
    assert config.category_to_terms is not None
    assert isinstance(config.aspect_terms, list)
    assert isinstance(config.category_to_terms, dict)
    assert all(isinstance(v, list) for v in config.category_to_terms.values())

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
