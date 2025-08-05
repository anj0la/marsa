import csv
import json
import re
from tqdm import tqdm
from matching import AspectMatch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dataclasses import dataclass

@dataclass 
class AspectSentiment:
    aspect_match: AspectMatch
    sentiment: str
    confidence: float | None = None
    
@dataclass
class AspectSentimentResult:
    text: str
    aspects: list[AspectSentiment]
    
class AspectSentimentAnalyzer:
    def __init__(self, analyzer_type: str = "vader", threshold: float = 0.05):
        self.analyzer_type = analyzer_type
        self.threshold = threshold
        self._setup_analyzer()
    
    def _setup_analyzer(self): # TODO: Add other sentiment analysis models, like transformers (BERT)
        if self.analyzer_type == "vader":
            self.analyzer = SentimentIntensityAnalyzer()
        
    def analyze_aspects(self, aspect_matches: list[AspectMatch], sentence: str) -> list[AspectSentiment]:
        scores = self.analyzer.polarity_scores(sentence)
        sentiment = self._classify_sentiment(scores['compound'])
        
        return [AspectSentiment(aspect_match=aspect, sentiment=sentiment, confidence=scores['compound']) 
                for aspect in aspect_matches]
            
    def _classify_sentiment(self, compound_score: float) -> str:
        if compound_score >= self.threshold:
            return 'positive'
        elif compound_score <= -self.threshold:
            return 'negative'
        else:
            return 'neutral'
