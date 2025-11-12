#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/navbar_batch_id.txt') as f:
    batch_id = f.read().strip()

# Get batch status
batch = client.batches.retrieve(batch_id)
print(f"Batch status: {batch.status}")

if batch.status != 'completed':
    print(f"Batch not completed yet. Current status: {batch.status}")
    exit(1)

# Download results
result_file_id = batch.output_file_id
result = client.files.content(result_file_id)
results = result.text.strip().split('\n')

# Parse results
translations = {}

for line in results:
    data = json.loads(line)
    custom_id = data['custom_id']

    # Parse custom_id: navbar_{lang}_{key}
    parts = custom_id.replace('navbar_', '').split('_', 1)
    lang_code = parts[0]
    string_key = parts[1]

    if data['response']['status_code'] == 200:
        translated_text = data['response']['body']['choices'][0]['message']['content']

        if lang_code not in translations:
            translations[lang_code] = {}

        translations[lang_code][string_key] = translated_text

# Add English strings
translations['en'] = {
    "about": "About",
    "docs": "Docs",
    "downloads": "Downloads",
    "blog": "Blog",
    "getInvolved": "Get Involved",
    "overview": "Overview",
    "researchPapers": "Research Papers",
    "press": "Press",
    "contactUs": "Contact Us",
    "featureSuggestions": "Feature Suggestions",
    "getI2P": "Get I2P",
}

# Update i18n files
i18n_dir = '/Users/dustinfields/git/i2p.www/i18n'

for lang_code, strings in translations.items():
    file_path = f'{i18n_dir}/{lang_code}.toml'

    # Read existing file if it exists
    existing_content = ''
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # Append nav section
    with open(file_path, 'a', encoding='utf-8') as f:
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write('\n[nav]\n')
        for key, value in strings.items():
            # Escape quotes and backslashes
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'{key} = "{escaped_value}"\n')

    print(f'Updated {file_path}')

print(f"\nCompleted navbar translation for {len(translations)} languages")
