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
    def __init__(self, analyzer_type: str = "vader", threshold: float = 0.05, context_window: int = 5) -> None:
        self.analyzer_type = analyzer_type
        self.threshold = threshold
        self.context_window = context_window
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.bert_model = pipeline(
            "sentiment-analysis", # alias for text-classication
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )
        self._setup_analyzer()
        self.doc = None
    
    def _setup_analyzer(self):
        if self.analyzer_type == "vader":
            self.analyzer = SentimentIntensityAnalyzer()
        elif self.analyzer_text == "bert":
            model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
            self.analyzer = pipeline(
                "sentiment-analysis", 
                model=model_name, 
                tokenizer=model_name,
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=True
            )
        
    def analyze_text(self, text: str, aspect_matches: list[AspectMatch], doc: Doc) -> AspectSentimentResult:
        self.doc = doc
        aspect_sentiments = []
        
        for aspect in aspect_matches:
            context = self._extract_context_window(text, aspect)
            
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
    
    def _weighted_sentiment(self, bert_probs: list[float], vader_score: float) -> tuple[str, float]:
        bert_sentiment_score = (
            -1 * bert_probs[0] +  # negative
             0 * bert_probs[1] +  # neutral  
             1 * bert_probs[2]    # positive
        )
        bert_confidence = max(bert_probs)  # highest probability
        vader_confidence = abs(vader_score)  # distance from neutral
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
    
    def _extract_bert_probabilities(self, bert_results) -> list[float]:        
        probs = [0.0, 0.0, 0.0]  # [negative, neutral, positive]
        
        for result in bert_results:
            label = result['label'].lower()
            score = result['score']
            
            if 'negative' in label:
                probs[0] = score
            elif 'neutral' in label:
                probs[1] = score
            elif 'positive' in label:
                probs[2] = score
        
        return probs