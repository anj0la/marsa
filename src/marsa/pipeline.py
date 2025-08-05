from marsa.config import load_aspect_config
from marsa.matching import match_aspect_phrases
from marsa.sentiment import AspectSentimentAnalyzer, AspectSentimentResult
from marsa.utils import clean_input

class AspectSentimentPipeline:
    def __init__(self, config_file: str):
        self.config = load_aspect_config(config_file)
        self.sentiment_analyzer = AspectSentimentAnalyzer()
    
    def process_corpus_flat(self, comments: list[str]) -> list[dict]:
        results = []
        for comment in comments:
            cleaned = clean_input(comment)
            aspects, doc = match_aspect_phrases(cleaned, self.config)
            sentiment_result = self.sentiment_analyzer.analyze_text(cleaned, aspects, doc)
            results.append({
                'original_text': comment,
                'cleaned_text': cleaned,
                'aspects_found': len(aspects),
                'aspect_sentiments': [
                    {
                        'aspect': aspect.aspect_match.text,
                        'category': aspect.aspect_match.category,
                        'sentiment': aspect.sentiment,
                        'confidence': aspect.confidence,
                        'start': aspect.aspect_match.start,
                        'end': aspect.aspect_match.end
                    }
                    for aspect in sentiment_result.aspects
                ]
            })
        return results
    
    def process_corpus(self, comments: list[str]) -> list[AspectSentimentResult]:
        results = []
        for comment in comments:
            cleaned = clean_input(comment)
            aspects, doc = match_aspect_phrases(cleaned, self.config)
            sentiment_result = self.sentiment_analyzer.analyze_text(cleaned, aspects, doc)
            results.append(sentiment_result)
        return results