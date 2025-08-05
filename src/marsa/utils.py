import emoji
import re
import spacy
import subprocess
import sys

def clean_input(text: str) -> str:
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'\w+@\w+\.com', '', text)
    text = emoji.demojize(text)
    text = re.sub(r':(.*?):')
    return text.strip()
    
def require_spacy_model(name: str = "en_core_web_sm"):
    try:
        return spacy.load(name)
    except OSError:
        print(f"Downloading spaCy model: {name}...")
        subprocess.run([sys.executable, "-m", "spacy", "download", name], check=True)
        return spacy.load(name)
