import torch
from marsa.matching import AspectMatch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dataclasses import dataclass
from transformers import pipeline
from spacy.tokens import Doc

@dataclass 
class AspectSentiment:
    aspect_match: AspectMatch
    sentiment: str
    confidence: float | None = None
    context_used: str | None = None
    
@dataclass
class AspectSentimentResult:
    text: str
    aspects: list[AspectSentiment]
    
class AspectSentimentAnalyzer:
    def __init__(self, threshold: float = 0.05, context_window: int = 5) -> None:
        self.threshold = threshold
        self.context_window = context_window
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.bert_model = pipeline(
            "sentiment-analysis", # alias for text-classication
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1,
            top_k=True
        )
        self.doc = None
        
    def analyze_text(self, text: str, aspect_matches: list[AspectMatch], doc: Doc) -> AspectSentimentResult:
        self.doc = doc  
        aspect_sentiments = []
        
        for aspect in aspect_matches:
            context = self._extract_context_window(aspect)
            
            vader_scores = self.vader_analyzer.polarity_scores(context)
            vader_compound = vader_scores['compound']
            bert_results = self.bert_model(context)[0]
            bert_probs = self._extract_bert_probabilities(bert_results)
            
            sentiment, confidence = self._weighted_sentiment(bert_probs, vader_compound)
            
            aspect_sentiments.append(AspectSentiment(
                aspect_match=aspect,
                sentiment=sentiment,
                confidence=confidence,
                context_used=context
            ))
        
        return AspectSentimentResult(text=text, aspects=aspect_sentiments)
    
    def _extract_context_window(self, aspect_match: AspectMatch) -> str:
        start_token = max(0, aspect_match.token_start - self.context_window)
        end_token = min(len(self.doc), aspect_match.token_end + self.context_window)
        return self.doc[start_token:end_token].text
    
    def _extract_bert_probabilities(self, bert_results: dict) -> list[float]:        
        probs = [0.0, 0.0, 0.0]  # [negative, neutral, positive]
        
        for result in bert_results:
            label = result['label'].lower()
            score = result['score']
            
            if 'negative' in label or label == 'label_0':
                probs[0] = score
            elif 'neutral' in label or label == 'label_1':
                probs[1] = score
            elif 'positive' in label or label == 'label_2':
                probs[2] = score
            
        return probs
    
    def _weighted_sentiment(self, bert_probs: list[float], vader_score: float) -> tuple[str, float]:
        bert_sentiment_score = (
            -1 * bert_probs[0] +   # negative
             0 * bert_probs[1] +   # neutral  
             1 * bert_probs[2]     # positive
        )
        bert_confidence = max(bert_probs)
        vader_confidence = abs(vader_score)
        total_confidence = bert_confidence + vader_confidence
        
        if total_confidence > 0:
            bert_weight = bert_confidence / total_confidence
            vader_weight = vader_confidence / total_confidence
        else:
            bert_weight = vader_weight = 0.5
        
        combined_score = (bert_weight * bert_sentiment_score) + (vader_weight * vader_score)
        
        agreement_factor = self._calculate_agreement(bert_sentiment_score, vader_score)
        final_confidence = agreement_factor * max(bert_confidence, vader_confidence)
        
        if combined_score > self.threshold:
            return "positive", final_confidence
        elif combined_score < -self.threshold:
            return "negative", final_confidence
        else:
            return "neutral", final_confidence
        
    def _calculate_agreement(self, bert_score: float, vader_score: float) -> float:
        if (bert_score > 0 and vader_score > 0) or (bert_score < 0 and vader_score < 0):
            return 1.0  # agreement
        elif abs(bert_score) < self.threshold and abs(vader_score) < self.threshold:
            return 1.0  # both neutral
        else:
            return 0.5  # disagreement
