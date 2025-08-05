import spacy
from spacy.matcher import PhraseMatcher
from config import AspectConfig
from dataclasses import dataclass
from utils import require_spacy_model

@dataclass
class AspectMatch:
    text: str
    start: int
    end: int   
    token_start: int
    token_end: int    
    category: str | None = None 

def match_aspect_phrases(text: str, config: AspectConfig) -> list[AspectMatch]:
    nlp = require_spacy_model("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    term_to_category = {}
    
    if config.aspect_terms:
        patterns = [nlp.make_doc(term) for term in config.aspect_terms]
        term_to_category = {term.lower(): None for term in config.aspect_terms}
    else:
        all_terms = []
        for category, terms in config.category_to_terms.items():
            for term in terms:
                all_terms.append(term)
                term_to_category[term.lower()] = category
        patterns = [nlp.make_doc(term) for term in all_terms]
    
    matcher.add('AspectTermsList', patterns)
            
    doc = nlp(text)
    matches = matcher(doc)
    
    aspects = []
    for _, start, end in matches:
        span = doc[start:end]
        category = term_to_category.get(span.text.lower(), None)

        aspects.append(AspectMatch(
            text=span.text, 
            start=span.start_char, 
            end=span.end_char,     
            token_start=start,      
            token_end=end,       
            category=category
        ))
    
    return aspects