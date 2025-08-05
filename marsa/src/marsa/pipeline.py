from config import AspectConfig, load_aspect_config
from matching import match_aspect_phrases
from sentiment import AspectSentimentAnalyzer
from utils import clean_input

class AspectSentimentPipeline:
    def __init__(self, config_file: str):
        self.config = load_aspect_config(config_file)
        self.sentiment_analyzer = AspectSentimentAnalyzer()
    
    def process_corpus(self, comments: list[str]) -> list[dict]:
        results = []
        for comment in comments:
            cleaned = clean_input(comment)
            aspects = match_aspect_phrases(cleaned, self.config)
            aspect_sentiments = self.sentiment_analyzer.analyze_aspects(aspects, cleaned)
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
                    for aspect in aspect_sentiments
                ]
            })
        return results