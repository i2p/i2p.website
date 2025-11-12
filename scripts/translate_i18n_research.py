#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Strings to translate
strings = {
    "contents": "Contents",
    "introduction": "Introduction",
    "notesToResearchers": "Notes to Researchers",
    "ethicsGuidelines": "Ethics & Guidelines",
    "researchQuestions": "Research Questions",
    "contact": "Contact"
}

# Languages (exclude English)
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
    for string_key, string_value in strings.items():
        batch_requests.append({
            "custom_id": f"{lang_code}_{string_key}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following text to {lang_name}. Only output the translation, nothing else. Preserve any markdown or HTML formatting."
                    },
                    {
                        "role": "user",
                        "content": string_value
                    }
                ],
                "max_tokens": 100
            }
        })

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/i18n_research.jsonl'
with open(batch_file, 'w') as f:
    for req in batch_requests:
        f.write(json.dumps(req) + '\n')

print(f"Created batch file with {len(batch_requests)} requests: {batch_file}")

# Submit batch
with open(batch_file, 'rb') as f:
    batch_input_file = client.files.create(file=f, purpose="batch")

batch = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "I2P research layout i18n translations"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/i18n_research_batch_id.txt', 'w') as f:
    f.write(batch.id)
