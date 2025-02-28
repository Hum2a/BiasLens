import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
from typing import Dict, List, Any
import spacy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Download required NLTK resources if not already downloaded
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('punkt')
except LookupError:
    nltk.download('punkt')

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Load spaCy language model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # If model not installed, download it
    print("Downloading spaCy language model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Political bias dictionaries - more comprehensive for better classification
left_leaning_keywords = [
    "progressive", "liberal", "democrat", "socialism", "social justice", 
    "equality", "diversity", "inclusion", "climate change", "renewable energy",
    "gun control", "abortion rights", "pro-choice", "LGBTQ+ rights", "universal healthcare",
    "tax the rich", "wealth tax", "welfare", "regulation", "union", "labor rights",
    "immigration reform", "racial justice", "defund police", "income inequality",
    "green new deal", "student loan forgiveness", "living wage"
]

right_leaning_keywords = [
    "conservative", "republican", "free market", "capitalism", "traditional values",
    "tax cuts", "deregulation", "second amendment", "pro-life", "religious freedom",
    "border security", "national security", "military spending", "law and order",
    "small government", "family values", "patriotism", "american exceptionalism",
    "tough on crime", "deficit reduction", "individual liberty", "personal responsibility",
    "school choice", "free speech", "constitutional originalism"
]

# News source bias reference
news_source_bias = {
    "CNN": "Left",
    "MSNBC": "Left",
    "NBC News": "Left",
    "New York Times": "Left",
    "Washington Post": "Left",
    "Huffington Post": "Left",
    "The Guardian": "Left",
    "Vox": "Left",
    "BuzzFeed": "Left",
    "Slate": "Left",
    "Fox News": "Right",
    "Breitbart": "Right",
    "The Daily Wire": "Right",
    "The Blaze": "Right",
    "National Review": "Right",
    "Washington Times": "Right",
    "NewsMax": "Right",
    "The Spectator": "Right",
    "New York Post": "Right",
    "Washington Examiner": "Right",
    "Reuters": "Center",
    "AP": "Center",
    "Associated Press": "Center",
    "BBC": "Center",
    "The Hill": "Center",
    "USA Today": "Center",
    "Bloomberg": "Center",
    "The Wall Street Journal": "Center",
    "The Economist": "Center",
    "CNBC": "Center",
    "Axios": "Center",
    "Financial Times": "Center",
    "NPR": "Center"
}

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text using spaCy."""
    if not text:
        return []
    
    doc = nlp(text)
    keywords = []
    
    # Get nouns and proper nouns
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
            keywords.append(token.text.lower())
    
    # Get noun phrases
    for chunk in doc.noun_chunks:
        keywords.append(chunk.text.lower())
    
    return list(set(keywords))

def calculate_bias_score(text: str) -> float:
    """
    Calculate political bias score from -1 (left) to 1 (right).
    0 represents center.
    """
    if not text:
        return 0.0
    
    text = text.lower()
    
    # Count occurrences of bias keywords
    left_count = sum(1 for keyword in left_leaning_keywords if keyword.lower() in text)
    right_count = sum(1 for keyword in right_leaning_keywords if keyword.lower() in text)
    
    # Calculate bias score between -1 and 1
    total_count = left_count + right_count
    if total_count == 0:
        return 0.0
    
    return (right_count - left_count) / total_count

def determine_political_bias(article: Dict[str, Any]) -> str:
    """
    Determine the political bias of an article.
    Returns "Left", "Right", or "Center"
    """
    # Check if we already know the source's bias
    source = article.get("source", "").strip()
    if source in news_source_bias:
        # Source has known bias, weight this heavily
        source_bias = news_source_bias[source]
        source_bias_score = 1.0 if source_bias == "Right" else (-1.0 if source_bias == "Left" else 0.0)
        weight_source = 0.6  # Source has 60% weight
    else:
        source_bias_score = 0.0
        weight_source = 0.0
    
    # Analyze content bias
    title = article.get("title", "")
    description = article.get("description", "")
    content_text = f"{title} {description}".lower()
    
    content_bias_score = calculate_bias_score(content_text)
    weight_content = 1.0 - weight_source  # Content has remaining weight
    
    # Weighted average of source and content bias
    final_bias_score = (source_bias_score * weight_source) + (content_bias_score * weight_content)
    
    # Determine bias category
    if final_bias_score < -0.2:
        return "Left"
    elif final_bias_score > 0.2:
        return "Right"
    else:
        return "Center"

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of a text using VADER.
    Returns sentiment score and label.
    """
    if not text:
        return {"score": 0.0, "label": "Neutral"}
    
    sentiment = sia.polarity_scores(text)
    compound_score = sentiment['compound']
    
    if compound_score >= 0.05:
        label = "Positive"
    elif compound_score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    
    return {
        "score": compound_score,
        "label": label
    }

def analyze_articles_with_bias(input_file: str, output_file: str) -> None:
    """
    Analyze political bias and sentiment of articles.
    """
    print(f"Analyzing articles from {input_file}...")
    
    try:
        with open(input_file, 'r') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"Error loading articles: {e}")
        return
    
    analyzed_articles = []
    
    for article in articles:
        try:
            # Get text to analyze
            title = article.get("title", "")
            description = article.get("description", "")
            analysis_text = f"{title} {description}"
            
            # Skip if no text to analyze
            if not analysis_text.strip():
                continue
                
            # Analyze sentiment
            sentiment_analysis = analyze_sentiment(analysis_text)
            
            # Determine political bias
            political_bias = determine_political_bias(article)
            
            # Create analyzed article
            analyzed_article = {
                **article,
                "sentiment": sentiment_analysis["label"],
                "sentiment_score": sentiment_analysis["score"],
                "political_bias": political_bias
            }
            
            analyzed_articles.append(analyzed_article)
            
        except Exception as e:
            print(f"Error analyzing article: {e}")
            continue
    
    print(f"Analyzed {len(analyzed_articles)} articles")
    print(f"Political bias distribution:")
    bias_counts = {"Left": 0, "Center": 0, "Right": 0}
    for article in analyzed_articles:
        bias = article.get("political_bias", "Unknown")
        if bias in bias_counts:
            bias_counts[bias] += 1
    
    for bias, count in bias_counts.items():
        percentage = (count / len(analyzed_articles)) * 100 if analyzed_articles else 0
        print(f"  {bias}: {count} ({percentage:.1f}%)")
    
    # Save analyzed articles
    try:
        with open(output_file, 'w') as f:
            json.dump(analyzed_articles, f, indent=4)
        print(f"Saved analyzed articles to {output_file}")
    except Exception as e:
        print(f"Error saving analyzed articles: {e}")
