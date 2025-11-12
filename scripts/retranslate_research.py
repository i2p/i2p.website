#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read the English source
with open('/Users/dustinfields/git/i2p.www/content/en/research.md', 'r') as f:
    english_content = f.read()

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
    batch_requests.append({
        "custom_id": f"research_{lang_code}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a professional translator specializing in technical documentation. Translate the following markdown content to {lang_name}. IMPORTANT: Preserve ALL markdown formatting, HTML tags, and front matter exactly as they appear. Only translate the actual text content, not the structure. Do not add any explanations or notes."
                },
                {
                    "role": "user",
                    "content": english_content
                }
            ],
            "max_tokens": 4000
        }
    })

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/research_retranslate.jsonl'
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
    metadata={"description": "I2P research page retranslation"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/research_retranslate_batch_id.txt', 'w') as f:
    f.write(batch.id)
