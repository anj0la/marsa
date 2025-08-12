import json
import yaml
from dataclasses import dataclass
from pathlib import Path
   
@dataclass 
class AspectData:
    phrases: list[str] | None = None
    category: str | None = None
     
@dataclass
class AspectConfig:
    aspects: dict[str, AspectData]
    
def create_aspect_config(file_path: str) -> AspectConfig:
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if path.suffix not in ('.yaml', '.yml', '.json'):
        raise NameError('Expected YAML (.yaml, .yml) or JSON (.json) extension.')
    
    with path.open('r', encoding='utf-8') as fp:
        if path.suffix in ('.yaml', '.yml'):
            data = yaml.safe_load(fp)
        else: # .json
            data = json.load(fp)

    aspects = {
        aspect_name: AspectData(
            phrases=aspect_data.get('phrases'),
            category=aspect_data.get('category')
        )
        for aspect_name, aspect_data in data.get('aspects', {}).items()
    }
    
    return AspectConfig(aspects=aspects)