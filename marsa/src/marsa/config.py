import json
import os
import yaml
from pathlib import Path

def load_from_yaml(file_path: str) -> list[dict]: 
    # Make sure that extension is valid
    if not check_file_extension(file_path, ['.yaml', '.yml']):
        raise NameError(f'Expected a YAML extension (.yaml, .yml).')
    
    path = Path(file_path).resolve()

    if path.exists():
        with path.open('r') as fp:
            return list(yaml.load_all(fp, Loader=yaml.SafeLoader))
    else:
        raise FileNotFoundError('File not found.')
            
def load_from_txt(file_path: str, has_categories=False) -> list[dict]:
    # Make sure that extension is valid
    if not check_file_extension(file_path, ['.txt']):
        raise NameError(f'Expected a TXT extension (.txt).')
    
    lines = []
    data = {}
    
    file_path = Path(file_path).resolve()

    if file_path.exists():    
        with file_path.open('r') as fp:
            lines = [line.strip() for line in fp.readlines()]
            
            if not has_categories:
                data['aspects'] = [line for line in lines]
                
            else:
                data['categories'] = {}
                for line in lines:
                    split = line.split(':')
                    category = split[0]
                    aspect_terms = split[1].strip().split(',')
                    data['categories'].setdefault(category, []).extend(aspect_terms)
            
            return [data]
                
    else:
        raise FileNotFoundError('File not found.')
        
def load_from_json(file_path: str) -> list[dict]:
    # Make sure that extension is valid
    if not check_file_extension(file_path, ['.json']):
        raise NameError(f'Expected a JSON extension (.json).')
    
    file_path = Path(file_path).resolve()
    fp = Path(file_path)

    if file_path.exists():
        with file_path.open('r') as fp:
            return json.load(fp)
    else:
        raise FileNotFoundError('File not found.')
    
def check_file_extension(file_path: str, expected_ext: list[str]) -> bool:
    path = Path(file_path)
    return any(path.suffix.lower() == ext.lower() for ext in expected_ext)