import json
import yaml
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AspectConfig:
    aspect_terms: list[str] | None = None
    category_to_terms: dict[str, list[str]] | None = None
    
def load_aspect_config(file_path: str) -> AspectConfig:
    if check_file_extension(file_path, ['.yaml', '.yml']):
        return load_from_yaml(file_path)
    elif check_file_extension(file_path, ['.json']):
        return load_from_json(file_path)
    else:
        raise NameError(f'Expected a YAML (.yaml, .yml) or JSON (.json) extension.')

def load_from_yaml(file_path: str) -> AspectConfig: 
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open('r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp)
        return AspectConfig(
            aspect_terms=data.get('aspect_terms'),
            category_to_terms=data.get('category_to_terms')
        )
            
def load_from_json(file_path: str) -> AspectConfig:
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open('r', encoding='utf-8') as fp:
        data = json.load(fp)
        return AspectConfig(
            aspect_terms=data.get('aspect_terms'),
            category_to_terms=data.get('category_to_terms')
        )
    
def check_file_extension(file_path: str, expected_ext: list[str]) -> bool:
    path = Path(file_path)
    return any(path.suffix.lower() == ext.lower() for ext in expected_ext)
