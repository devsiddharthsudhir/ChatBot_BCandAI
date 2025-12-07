from pathlib import Path
import json

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from joblib import dump

# Ensure required NLTK resources
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

BASE_DIR = Path(__file__).resolve().parent.parent
INTENTS_PATH = BASE_DIR / "data" / "intents.json"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

def preprocess(text: str) -> str:
    text = text.lower()
    tokens = word_tokenize(text)
    sw = set(stopwords.words("english"))
    filtered = [t for t in tokens if t.isalpha() and t not in sw]
    return " ".join(filtered)

def load_data():
    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    texts, labels = [], []
    for intent in data["intents"]:
        tag = intent["tag"]
        for pattern in intent["patterns"]:
            texts.append(preprocess(pattern))
            labels.append(tag)
    return texts, labels

def main():
    texts, labels = load_data()
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    clf = LinearSVC()
    clf.fit(X, labels)

    dump(vectorizer, MODEL_DIR / "vectorizer.joblib")
    dump(clf, MODEL_DIR / "classifier.joblib")
    print("✅ Training complete. Models saved in", MODEL_DIR)

if __name__ == "__main__":
    main()
