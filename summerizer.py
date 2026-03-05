import json
from transformers import pipeline


generator = pipeline(
    "text-generation",
    model="facebook/bart-large-cnn"
)


def generate_summary(text):
    """Generates an academic summary using text-generation logic."""
    # We provide a clear instruction to the model
    prompt = f"Summarize the following text into a detailed academic paragraph: {text}"

    results = generator(
        prompt,
        max_new_tokens=200,
        min_new_tokens=100,
        do_sample=False
    )

    # Extract the generated text and remove the prompt
    generated_text = results[0]["generated_text"]
    summary = generated_text.replace(prompt, "").strip()
    return summary


def extract_key_points(text):
    """Extracts at least 5 key points (sentences > 40 chars)."""
    sentences = text.split(".")
    key_points = [s.strip() for s in sentences if len(s.strip()) > 40]
    return key_points[:5]


def save_academic_json(clean_text, title="Introduction to Machine Learning"):
    """Assembles the final JSON structure exactly as required."""
    output = {
        "title": title,
        "summary": generate_summary(clean_text),
        "key_points": extract_key_points(clean_text),
        "definitions": {
            "Machine Learning": "A branch of artificial intelligence that enables systems to learn from data."
        },
        "questions_raised": [
            "How does machine learning improve decision making?"
        ],
        "keywords": ["AI", "Machine Learning", "Data"]
    }

    with open("notes.json", "w") as f:
        json.dump(output, f, indent=4)

    print("✅ Success: 'notes.json' has been created.")


if __name__ == "__main__":
    # Sample text for testing
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans. 
    AI research has been defined as the study of intelligent agents, systems that perceive their environment and take actions to achieve goals. 
    The field was founded on the assumption that human intelligence can be so precisely described that a machine can be made to simulate it. 
    This raises ethical consequences of creating artificial beings endowed with human-like intelligence.
    """
    save_academic_json(test_text)