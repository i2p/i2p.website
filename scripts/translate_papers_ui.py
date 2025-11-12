#!/usr/bin/env python3
"""
Translate only the UI elements in papers.html (PDF button, Show BibTeX).
Leaves paper titles, authors, and venues in original language.
"""
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# UI strings to translate in papers.html
ui_strings = {
    "pdf": "PDF",
    "showBibtex": "Show BibTeX",
}

# Languages
languages = {
    'de': 'German',
    'es': 'Spanish',
    'ko': 'Korean',
    'ru': 'Russian',
    'cs': 'Czech',
    'fr': 'French',
    'tr': 'Turkish',
    'zh': 'Chinese',
    'vi': 'Vietnamese',
    'hi': 'Hindi',
    'ar': 'Arabic',
    'pt': 'Portuguese'
}

# Create batch requests
batch_requests = []

for lang_code, lang_name in languages.items():
    for string_key, string_value in ui_strings.items():
        batch_requests.append({
            "custom_id": f"papers_ui_{lang_code}_{string_key}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate this UI button text to {lang_name}. Keep it very short and concise. Only output the translation."
                    },
                    {
                        "role": "user",
                        "content": string_value
                    }
                ],
                "max_tokens": 50
            }
        })

print(f"Total UI strings: {len(ui_strings)}")
print(f"Total languages: {len(languages)}")
print(f"Total requests: {len(batch_requests)}")

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/papers_ui.jsonl'
os.makedirs(os.path.dirname(batch_file), exist_ok=True)

with open(batch_file, 'w') as f:
    for req in batch_requests:
        f.write(json.dumps(req) + '\n')

print(f"\nCreated batch file: {batch_file}")

# Submit batch
with open(batch_file, 'rb') as f:
    batch_input_file = client.files.create(file=f, purpose="batch")

batch = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "I2P papers UI i18n"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/papers_ui_batch_id.txt', 'w') as f:
    f.write(batch.id)

print("\nNote: This only translates UI elements (PDF, Show BibTeX).")
print("Paper titles, authors, and venues remain in original language.")
print("To apply translations, we'll need to update the papers layout template.")
