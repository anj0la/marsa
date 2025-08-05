from marsa.config import AspectConfig
from marsa.matching import match_aspect_phrases, AspectMatch
from tests.constants import ASPECT_CONFIG

# ---------- Regular Tests ----------

def test_match_aspect_phrases_basic():
    # Arrange
    text = "I love the camera but hate the battery life"
    
    # Act
    aspects, _ = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 2
    assert all(isinstance(aspect, AspectMatch) for aspect in aspects)
    
    # Check first match (camera)
    camera_match = aspects[0]
    assert camera_match.text == "camera"
    assert camera_match.start == 11
    assert camera_match.end == 17
    assert camera_match.token_start == 3
    assert camera_match.token_end == 4
    assert camera_match.category == "hardware"
    
    # Check second match (battery)
    battery_match = aspects[1]
    assert battery_match.text == "battery"
    assert battery_match.start == 31
    assert battery_match.end == 38
    assert battery_match.token_start == 7
    assert battery_match.token_end == 8
    assert battery_match.category == "hardware"

def test_match_aspect_phrases_returns_doc():
    # Arrange
    text = "I love the camera but hate the battery life"
    
    # Act
    _, doc = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert doc is not None
    assert hasattr(doc, 'text')
    assert doc.text == text
    assert len(doc) > 0

def test_match_aspect_phrases_no_matches():
    # Arrange
    text = "This is a simple sentence with no relevant terms"
    
    # Act
    aspects, doc = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 0
    assert doc is not None
    assert doc.text == text

def test_match_aspect_phrases_multiple_same_term():
    # Arrange
    text = "The camera quality is good, but the camera settings are confusing"
    
    # Act
    aspects, _ = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 2
    assert all(aspect.text == "camera" for aspect in aspects)
    assert all(aspect.category == "hardware" for aspect in aspects)
    assert aspects[0].start != aspects[1].start
    assert aspects[0].end != aspects[1].end

def test_match_aspect_phrases_case_insensitive():
    # Arrange
    text = "I love the CAMERA but hate the Battery life"
    
    # Act
    aspects, doc = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 2
    
    camera_match = next(aspect for aspect in aspects if aspect.text.lower() == "camera")
    battery_match = next(aspect for aspect in aspects if aspect.text.lower() == "battery")
    
    assert camera_match.category == "hardware"
    assert battery_match.category == "hardware"

def test_match_aspect_phrases_aspect_terms_only():
    # Arrange
    from marsa.config import AspectConfig
    config = AspectConfig(aspect_terms=["camera", "battery", "screen"])
    text = "The camera and screen are great"
    
    # Act
    aspects, _ = match_aspect_phrases(text, config)
    
    # Assert
    assert len(aspects) == 2
    assert all(aspect.category is None for aspect in aspects)
    
    terms_found = [aspect.text for aspect in aspects]
    assert "camera" in terms_found
    assert "screen" in terms_found

# ---------- Edge Cases ----------

def test_match_aspect_phrases_empty_text():
    # Arrange
    text = ""
    
    # Act
    aspects, doc = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 0
    assert doc is not None
    assert doc.text == ""

def test_match_aspect_phrases_whitespace_only():
    # Arrange
    text = "   \n\t  "
    
    # Act
    aspects, doc = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 0
    assert doc is not None

def test_match_aspect_phrases_punctuation_handling():
    # Arrange
    text = "The camera, battery, and screen work well!"
    
    # Act
    aspects, _ = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 3
    terms_found = [aspect.text for aspect in aspects]
    assert "camera" in terms_found
    assert "battery" in terms_found  
    assert "screen" in terms_found

def test_match_aspect_phrases_partial_word_no_match():
    # Arrange
    text = "The cameras and batteries are working"
    
    # Act
    aspects, _ = match_aspect_phrases(text, ASPECT_CONFIG)
    
    # Assert
    assert len(aspects) == 0

def test_match_aspect_phrases_empty_config():
    # Arrange
    config = AspectConfig(aspect_terms=[], category_to_terms={})
    text = "The camera and battery are good"
    
    # Act
    aspects, doc = match_aspect_phrases(text, config)
    
    # Assert
    assert len(aspects) == 0
    assert doc is not None