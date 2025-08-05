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
    elif check_file_extension(file_path, ['.txt']):
        return load_from_txt(file_path)
    elif check_file_extension(file_path, ['.json']):
        return load_from_json(file_path)
    else:
        raise NameError(f'Expected a YAML (.yaml, .yml), TXT (.txt) or JSON (.json) extension.')

def load_from_yaml(file_path: str) -> AspectConfig: 
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open('r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp)
        return AspectConfig(
            aspect_terms=data.get('aspects'),
            category_to_terms=data.get('categories')
        )
            
def load_from_txt(file_path: str) -> AspectConfig:    
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with path.open('r', encoding='utf-8') as fp:
        lines = [line.strip() for line in fp if line.strip()]

        # Detect if format has categories by checking for colon presence
        if any(':' in line for line in lines):
            category_to_terms = {}
            for line in lines:
                if ':' not in line:
                    continue  # skip malformed line
                category, terms = line.split(':', 1)
                aspect_terms = [t.strip() for t in terms.split(',') if t.strip()]
                category_to_terms.setdefault(category.strip(), []).extend(aspect_terms)
            return AspectConfig(
                category_to_terms=category_to_terms
            )
        else:
            return AspectConfig(
                aspect_terms=lines
            )
        
def load_from_json(file_path: str) -> AspectConfig:
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open('r', encoding='utf-8') as fp:
        data = json.load(fp)
        return AspectConfig(
            aspect_terms=data.get('aspects'),
            category_to_terms=data.get('categories')
        )
    
def check_file_extension(file_path: str, expected_ext: list[str]) -> bool:
    path = Path(file_path)
    return any(path.suffix.lower() == ext.lower() for ext in expected_ext)
