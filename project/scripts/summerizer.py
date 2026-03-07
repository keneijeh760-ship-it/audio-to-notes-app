import json
from pathlib import Path
from transformers import pipeline
import spacy
from collections import Counter

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]

CLEAN_TXT = BASE_DIR / "transcripts" / "lecture_cleaned.txt"
OUTPUT_JSON = BASE_DIR / "transcripts" / "notes.json"

# =========================
# LOAD MODELS
# =========================
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
nlp = spacy.load("en_core_web_sm")

# =========================
# SUMMARY
# =========================
def generate_summary(text):
    result = summarizer(
        text,
        max_length=2000,
        min_length=80,
        do_sample=False
    )
    return result[0]["summary_text"]

# =========================
# KEY POINTS
# =========================
def extract_key_points(text):
    doc = nlp(text)

    sentences = [
        sent.text.strip()
        for sent in doc.sents
        if len(sent.text.strip()) > 40
    ]

    return sentences[:5]

# =========================
# KEYWORD EXTRACTION
# =========================
def extract_keywords(text):

    doc = nlp(text)

    nouns = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN"]
        and not token.is_stop
        and len(token.text) > 3
    ]

    common = Counter(nouns).most_common(5)

    return [word for word, _ in common]

# =========================
# BASIC DEFINITIONS
# looks for sentences like
# "X is ..."
# =========================
def extract_definitions(text):

    doc = nlp(text)
    definitions = {}

    for sent in doc.sents:
        if " is " in sent.text.lower() and len(definitions) < 3:

            words = sent.text.split(" is ")

            if len(words) >= 2:
                term = words[0].strip().split()[-1]
                definition = words[1].strip()

                if len(term) > 2:
                    definitions[term] = definition

    return definitions

# =========================
# QUESTIONS FROM KEY POINTS
# =========================
def generate_questions(key_points):

    questions = []

    for point in key_points[:3]:
        questions.append(f"What is the significance of: {point[:80]}?")

    return questions

# =========================
# GENERATE TITLE
# =========================
def generate_title(keywords):

    if keywords:
        return "Lecture on " + keywords[0].capitalize()

    return "Lecture Notes"

# =========================
# CREATE JSON
# =========================
def save_academic_json(text):

    summary = generate_summary(text)
    key_points = extract_key_points(text)
    keywords = extract_keywords(text)
    definitions = extract_definitions(text)
    questions = generate_questions(key_points)
    title = generate_title(keywords)

    output = {
        "title": title,
        "summary": summary,
        "key_points": key_points,
        "definitions": definitions,
        "questions_raised": questions,
        "keywords": keywords
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("✅ notes.json created successfully")

# =========================
# MAIN
# =========================
if __name__ == "__main__":

    with open(CLEAN_TXT, "r", encoding="utf-8") as f:
        clean_text = f.read()

    save_academic_json(clean_text)