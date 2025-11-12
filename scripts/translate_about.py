#!/usr/bin/env python3
import os
import glob
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Get all .md files in about directory
about_dir = '/Users/dustinfields/git/i2p.www/content/en/about/'
md_files = glob.glob(os.path.join(about_dir, '*.md'))

# Get just the filenames (not full paths)
about_files = [os.path.basename(f) for f in md_files]

print(f"Found {len(about_files)} markdown files to translate")

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

for filename in about_files:
    # Read the English source
    full_path = os.path.join(about_dir, filename)
    with open(full_path, 'r', encoding='utf-8') as f:
        english_content = f.read()

    # Create translation request for each language
    for lang_code, lang_name in languages.items():
        # Create safe custom_id
        custom_id = f"{lang_code}_about_{filename.replace('.md', '').replace('-', '_')}"

        batch_requests.append({
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator specializing in technical documentation. Translate the following markdown content to {lang_name}. IMPORTANT: Preserve ALL markdown formatting, HTML tags, code blocks, and front matter exactly. Only translate the text content, not code or technical identifiers. Do not add explanations."
                    },
                    {
                        "role": "user",
                        "content": english_content
                    }
                ],
                "max_tokens": 16000
            }
        })

print(f"Total files: {len(about_files)}")
print(f"Total languages: {len(languages)}")
print(f"Total requests: {len(batch_requests)}")

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/about.jsonl'
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
    metadata={"description": "I2P about translation"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID and file mapping
with open('/Users/dustinfields/git/i2p.www/scripts/about_batch_id.txt', 'w') as f:
    f.write(batch.id)

# Save file mapping for processing
with open('/Users/dustinfields/git/i2p.www/scripts/about_files.json', 'w') as f:
    json.dump(about_files, f)
