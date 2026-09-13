import os
import json
from google import genai
from vocabulary.models import Vocabulary
import time
from google.genai import errors


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def generate_words():
    prompt = """
Generate exactly 5 English vocabulary words for a daily
English-learning app.

Requirements:

- Words should be useful for everyday English.
- Do not generate offensive or inappropriate words.
- Do not generate very long words.
- Do not generate extremely advanced words.
- Prefer intermediate-level vocabulary.
- Each word must be different.
- Return exactly 5 words.

For each word provide:

- word
- pronunciation
- part_of_speech
- bangla_meaning
- definition
- example_sentence
- difficulty
- category

Return ONLY a valid JSON array.

The response must have exactly this structure:

[
  {
    "word": "example",
    "pronunciation": "ig-ZAM-pul",
    "part_of_speech": "noun",
    "bangla_meaning": "উদাহরণ",
    "definition": "Something used to explain or illustrate an idea.",
    "example_sentence": "This is a good example of teamwork.",
    "difficulty": "intermediate",
    "category": "general"
  }
]
"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            words = json.loads(response.text)

            return words

        except errors.ServerError as error:
            if attempt == max_retries - 1:
                raise

            time.sleep(2)

def save_generated_words(words):
    saved_words = []

    for word_data in words:
        if len(saved_words) >= 5:
            break

        word = word_data["word"].strip()
        normalized_word = word.lower()

        if Vocabulary.objects.filter(
            normalized_word=normalized_word
        ).exists():
            continue

        vocabulary = Vocabulary.objects.create(
            word=word,
            normalized_word=normalized_word,
            pronunciation=word_data["pronunciation"],
            part_of_speech=word_data["part_of_speech"],
            bangla_meaning=word_data["bangla_meaning"],
            definition=word_data["definition"],
            example_sentence=word_data["example_sentence"],
            difficulty=word_data["difficulty"],
            category=word_data["category"],
            source="gemini",
            generated_by="gemini-3.6-flash",
            generation_version="v1",
        )

        saved_words.append(vocabulary)

    return saved_words

def generate_and_save_words():
    saved_words = []

    while len(saved_words) < 5:
        words = generate_words()

        new_words = save_generated_words(words)

        saved_words.extend(new_words)

    return saved_words[:5]