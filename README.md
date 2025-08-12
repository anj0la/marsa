# MARSA

MARSA is a lightweight tool designed to streamline aspect-based sentiment analysis (ABSA) by automating the extraction and pre-labeling of aspect-sentiment pairs from review-style text. MARSA combines rule-based aspect extraction with sentiment analysis to accelerate the long process of manually labeling text data. It is especially useful for analyzing social media content such as Reddit comments and Twitter posts and mining product reviews from platforms like Amazon and Yelp.

The tool simplifies ABSA by identifying multiple aspects within a single sentence and automatically assigning initial sentiment scores using VADER. Users can define custom aspect terms and categories to tailor the analysis to their needs. MARSA also supports exporting results in JSON or CSV formats for easy manual review or use in training models. It can be accessed via command line or Python API, offering convenient ways to interact with it.

## How It Works

MARSA follows a simple four-step process to support aspect-based sentiment analysis:

1. **Configure aspects** - Define the aspects and categories you want to extract
2. **Process text** - MARSA finds aspects and assigns preliminary sentiment scores
3. **Review & correct** - Export results for manual verification
4. **Train models** - Use the labeled data to train custom ABSA models

## Installation

### Using pip
```bash
pip install marsa
```

### Using uv
```bash
uv add marsa
```

## Quick Start

### Command Line
```bash
# Analyze a file of comments (one per line)
marsa analyze comments.txt --config aspects.yaml --output results.json
```

### Python API
```python
from marsa import AspectSentimentPipeline

pipeline = AspectSentimentPipeline("aspects.yaml")
results = pipeline.process_corpus(["I love the camera but hate the battery life"])
```

## Configuration

The easiest way to configure MARSA is by using a YAML file. Create a `config.yaml` fine and define your aspects:
```yaml
aspects:
    camera:
        phrases: ["camera", "photo", "picture", "pics", "photography", "image", "snap"]
        category: "hardware"
    
    battery:
        phrases: ["battery", "power", "charge", "charging", "juice", "drain", "life"]
        category: "hardware"
    
    screen:
        phrases: ["screen", "display", "resolution", "brightness", "monitor", "lcd", "oled"]
        category: "interface"
```

You can define aspects by creating a `config.json` file as well:
```json
{
  "aspects": {
        "camera": {
            "phrases": ["camera", "photo", "picture", "pics", "photography", "image", "snap"],
            "category": "hardware"
        },
        "battery": {
            "phrases": ["battery", "power", "charge", "charging", "juice", "drain", "life"],
            "category": "hardware"
        },
        "screen": {
            "phrases": ["screen", "display", "resolution", "brightness", "monitor", "lcd", "oled"],
            "category": "interface"
        }
    }
}
```
