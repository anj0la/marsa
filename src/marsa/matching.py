from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
from marsa.config import AspectConfig
from dataclasses import dataclass
from marsa.utils import require_spacy_model

@dataclass
class AspectMatch:
    text: str       # actual text matches
    aspect: str     # the aspect it represents
    start: int
    end: int   
    token_start: int
    token_end: int    
    category: str | None = None 

def match_aspect_phrases(text: str, config: AspectConfig) -> tuple[list[AspectMatch], Doc]:
    nlp = require_spacy_model("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    phrase_to_aspect = {}
    patterns = [] 
    
    for aspect_name, aspect_data in config.aspects.items():
        if aspect_data.phrases:
            for phrase in aspect_data.phrases:
                patterns.append(nlp.make_doc(phrase))
                phrase_to_aspect[phrase.lower()] = aspect_name
        else:
            # If no phrases defined, use aspect name itself as the phrase
            patterns.append(nlp.make_doc(aspect_name))
            phrase_to_aspect[aspect_name.lower()] = aspect_name
    
    if patterns:
        matcher.add('AspectTermsList', patterns)
            
    doc = nlp(text)
    matches = matcher(doc)
    
    aspects = []
    for _, start, end in matches:
        span = doc[start:end]
        aspect_name = phrase_to_aspect[span.text.lower()]
        aspect_data = config.aspects[aspect_name]

        aspects.append(AspectMatch(
            text=span.text, 
            aspect=aspect_name,
            start=span.start_char, 
            end=span.end_char,     
            token_start=start,      
            token_end=end,       
            category=aspect_data.category
        ))
    
    return aspects, doc