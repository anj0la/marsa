import emoji
import re

def clean_input(text: str) -> str:
    text = text.lower()
    
    # Remove URLs, emails and links
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'\w+@\w+\.com', '', text)
  
    # Convert emojis to text
    text = emoji.demojize(text)
    text = re.sub(r':(.*?):')
   
    return text.strip()
    
