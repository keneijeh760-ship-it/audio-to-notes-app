import spacy

nlp = spacy.load("en_core_web_sm")

def read_transcript(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def clean_transcript(raw_text):
    doc = nlp(raw_text)

    cleaned_sentences = [
        sent.text.strip()
        for sent in doc.sents
        if len(sent.text.strip()) > 20
    ]

    return " ".join(cleaned_sentences)

# RUN THE PIPELINE
raw_text = read_transcript("transcript_project/lecture.txt")

clean_text = clean_transcript(raw_text)

# SAVE TO FILE
with open("cleaned_lecture.txt", "w", encoding="utf-8") as file:
    file.write(clean_text)

print("✅ Cleaned transcript saved as cleaned_lecture.txt")



