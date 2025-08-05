#from marsa.config import AspectConfig
from marsa.src.marsa.matching import AspectConfig, AspectMatch
from marsa.src.marsa.sentiment import AspectSentiment, AspectSentimentResult

EXAMPLE_CORPUS = ["I love the camera but hate the battery life"]

ASPECT_CONFIG = AspectConfig(
    aspect_terms=["camera", "battery", "screen"],
    category_to_terms={"hardware": ["camera", "battery"], "interface": ["screen"]}
)

FIRST_ASPECT_MATCH = AspectMatch(
    text = EXAMPLE_CORPUS[0],
    start = 11,
    end = 17,
    token_start = 3,
    token_end = 4,
    category = "hardware"
    )

SECOND_ASPECT_MATCH = AspectMatch(
    text = EXAMPLE_CORPUS[0],
    start = 31,
    end = 38,
    token_start = 7,
    token_end = 8,
    category = "hardware"
)

FIRST_ASPECT_SENTIMENT = AspectSentiment(
    aspect_match=FIRST_ASPECT_MATCH,
    sentiment = "positive",
    confidence = 0.9
)

SECOND_ASPECT_SENTIMENT = AspectSentiment(
    aspect_match=FIRST_ASPECT_MATCH,
    sentiment = "negative",
    confidence = 0.9
)

ASPECT_SENTIMENT_RESULT = AspectSentimentResult(
    text = EXAMPLE_CORPUS[0],
    aspects=[FIRST_ASPECT_SENTIMENT, SECOND_ASPECT_SENTIMENT]
)

