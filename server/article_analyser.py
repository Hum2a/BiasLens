import json
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Source bias mapping
SOURCE_BIAS = {
    "NY Times": "Left",
    "The Guardian": "Left",
    "Fox News": "Right",
    "CNN": "Left",
    "Google News": "Center",
    "MediaStack": "Center",
    "Currents": "Center",
}

BIAS_SCORE = {
    "Left": -1,
    "Center": 0,
    "Right": 1
}

LEFT_KEYWORDS = ["equality", "climate change", "universal healthcare", "social justice"]
RIGHT_KEYWORDS = ["freedom", "tax cuts", "border security", "gun rights"]

def analyze_sentiment(text):
    """
    Perform sentiment analysis on the given text using VADER.
    Returns a sentiment category and score.
    """
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']  # Overall sentiment score
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, compound

def calculate_keyword_bias(text):
    left_score = sum(text.lower().count(word) for word in LEFT_KEYWORDS)
    right_score = sum(text.lower().count(word) for word in RIGHT_KEYWORDS)

    if left_score > right_score:
        return "Left", left_score - right_score
    elif right_score > left_score:
        return "Right", right_score - left_score
    else:
        return "Center", 0

def determine_political_bias(article):
    # Source bias
    source_bias = SOURCE_BIAS.get(article.get("source"), "Center")
    source_bias_score = BIAS_SCORE.get(source_bias, 0)

    # Content analysis
    title = article.get("title") or ""  # Handle None values
    description = article.get("description") or ""  # Handle None values
    content = (title + " " + description).strip()
    _, keyword_bias_score = calculate_keyword_bias(content)
    sentiment_bias_score = article.get("sentiment_score", 0)

    # Combine weights
    final_score = 0.5 * source_bias_score + 0.3 * keyword_bias_score + 0.2 * sentiment_bias_score

    if final_score > 0.2:
        return "Right"
    elif final_score < -0.2:
        return "Left"
    else:
        return "Center"


def analyze_articles_with_bias(input_file, output_file):
    """
    Analyze sentiment and determine political bias for each article.
    """
    # Load articles
    with open(input_file, "r") as file:
        articles = json.load(file)

    # Analyze each article
    for article in articles:
        # Sentiment Analysis
        title = article.get("title") or ""
        description = article.get("description") or ""
        content = (title + " " + description).strip()

        if content:
            sentiment, score = analyze_sentiment(content)
            article["sentiment"] = sentiment
            article["sentiment_score"] = score
        else:
            article["sentiment"] = "Unanalyzable"
            article["sentiment_score"] = None

        # Political Bias
        article["political_bias"] = determine_political_bias(article)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save analyzed articles
    with open(output_file, "w") as file:
        json.dump(articles, file, indent=4)

    print(f"Analyzed {len(articles)} articles with political bias and saved results to {output_file}.")
