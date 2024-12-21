import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
import json

# Download NLTK data
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Stopwords
stop_words = set(stopwords.words("english"))

# Preprocessing function
def preprocess_text(text):
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    
    # 3. Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    
    # 4. Tokenize
    tokens = word_tokenize(text)
    
    # 5. Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    
    # 6. Lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Rejoin tokens into a single string
    return " ".join(tokens)

# Preprocess articles
def preprocess_articles(input_file, output_file):
    with open(input_file, "r") as file:
        articles = json.load(file)
    
    for article in articles:
        # Preprocess title and description
        article["title_cleaned"] = preprocess_text(article.get("title", ""))
        article["description_cleaned"] = preprocess_text(article.get("description", ""))
    
    # Save preprocessed data
    with open(output_file, "w") as file:
        json.dump(articles, file, indent=4)
    print(f"Preprocessed articles saved to {output_file}")

if __name__ == "__main__":
    preprocess_articles("../data/all_articles.json", "../data/preprocessed_articles.json")
