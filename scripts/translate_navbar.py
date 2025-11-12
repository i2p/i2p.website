#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# All the hardcoded strings in the navbar
navbar_strings = {
    # Main navigation
    "about": "About",
    "docs": "Docs",
    "downloads": "Downloads",
    "blog": "Blog",
    "getInvolved": "Get Involved",

    # Dropdown items
    "overview": "Overview",
    "researchPapers": "Research Papers",
    "press": "Press",
    "contactUs": "Contact Us",
    "featureSuggestions": "Feature Suggestions",

    # CTA button
    "getI2P": "Get I2P",
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
    for string_key, string_value in navbar_strings.items():
        batch_requests.append({
            "custom_id": f"navbar_{lang_code}_{string_key}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator specializing in website navigation and UI text. Translate the following navigation menu item to {lang_name}. Keep it concise and natural for a navigation menu. Only output the translation, nothing else. Keep technical terms like 'I2P' unchanged."
                    },
                    {
                        "role": "user",
                        "content": string_value
                    }
                ],
                "max_tokens": 100
            }
        })

print(f"Total strings: {len(navbar_strings)}")
print(f"Total languages: {len(languages)}")
print(f"Total requests: {len(batch_requests)}")

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/navbar.jsonl'
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
    metadata={"description": "I2P navbar i18n"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/navbar_batch_id.txt', 'w') as f:
    f.write(batch.id)
