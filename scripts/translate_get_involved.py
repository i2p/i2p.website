#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Files to translate
files = [
    'get-involved/_index.md',
    'get-involved/roadmap.md',
    'get-involved/guides/translator-guide.md'
]

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

for file_path in files:
    # Read the English source
    full_path = f'/Users/dustinfields/git/i2p.www/content/en/{file_path}'
    with open(full_path, 'r', encoding='utf-8') as f:
        english_content = f.read()

    # Create translation request for each language
    for lang_code, lang_name in languages.items():
        # Create safe custom_id by replacing slashes and dots
        custom_id = f"{lang_code}_{file_path.replace('/', '_').replace('.md', '')}"

        batch_requests.append({
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator specializing in technical documentation. Translate the following markdown content to {lang_name}. IMPORTANT: Preserve ALL markdown formatting, HTML tags, and front matter exactly. Only translate the text content. Do not add explanations."
                    },
                    {
                        "role": "user",
                        "content": english_content
                    }
                ],
                "max_tokens": 4000
            }
        })

print(f"Total files: {len(files)}")
print(f"Total languages: {len(languages)}")
print(f"Total requests: {len(batch_requests)}")

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/get_involved.jsonl'
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
    metadata={"description": "I2P get-involved pages translation"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/get_involved_batch_id.txt', 'w') as f:
    f.write(batch.id)
