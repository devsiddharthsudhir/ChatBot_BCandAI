from pathlib import Path
import json
import random

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from joblib import load

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

BASE_DIR = Path(__file__).resolve().parent.parent
INTENTS_PATH = BASE_DIR / "data" / "intents.json"
VECTORIZER_PATH = BASE_DIR / "models" / "vectorizer.joblib"
CLASSIFIER_PATH = BASE_DIR / "models" / "classifier.joblib"

MODEL_VERSION = "v1.0"
DATASET_ID = "intents_v1"

vectorizer = load(VECTORIZER_PATH)
classifier = load(CLASSIFIER_PATH)

with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents_data = json.load(f)["intents"]

TAG_TO_RESPONSES = {i["tag"]: i["responses"] for i in intents_data}

def preprocess(text: str) -> str:
    text = text.lower()
    tokens = word_tokenize(text)
    sw = set(stopwords.words("english"))
    filtered = [t for t in tokens if t.isalpha() and t not in sw]
    return " ".join(filtered)

def predict_intent(user_text: str) -> str:
    cleaned = preprocess(user_text)
    X = vectorizer.transform([cleaned])
    return classifier.predict(X)[0]

def get_response(user_text: str):
    tag = predict_intent(user_text)
    responses = TAG_TO_RESPONSES.get(
        tag, ["I'm not sure I understood that. Could you rephrase?"]
    )
    reply = random.choice(responses)
    meta = {
        "intent_tag": tag,
        "model_version": MODEL_VERSION,
        "dataset_id": DATASET_ID,
    }
    return reply, meta
