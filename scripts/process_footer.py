#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/footer_batch_id.txt') as f:
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

    # Parse custom_id: footer_{lang}_{key}
    parts = custom_id.replace('footer_', '').split('_', 1)
    lang_code = parts[0]
    string_key = parts[1]

    if data['response']['status_code'] == 200:
        translated_text = data['response']['body']['choices'][0]['message']['content']

        if lang_code not in translations:
            translations[lang_code] = {}

        translations[lang_code][string_key] = translated_text

# Add English strings
translations['en'] = {
    "newsletterDescription": "Stay updated with I2P news:",
    "subscribe": "Subscribe",
    "emailPlaceholder": "Enter your email",
    "quickLinks": "Quick Links",
    "donate": "Donate",
    "i2pIntroduction": "I2P Introduction",
    "community": "Community",
    "getInvolved": "Get Involved",
    "blog": "Blog",
    "officialForums": "Official Forums",
    "contact": "Contact",
    "resources": "Resources",
    "i2pMetrics": "I2P Metrics",
    "research": "Research",
    "gitlab": "GitLab",
    "stormycloud": "StormyCloud",
    "copyrightText": "The Invisible Internet Project. Licensed under Creative Commons.",
    "privacy": "Privacy",
    "terms": "Terms",
    "impressum": "Impressum",
    "press": "Press",
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

    # Append footer section
    with open(file_path, 'a', encoding='utf-8') as f:
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write('\n[footer]\n')
        for key, value in strings.items():
            # Escape quotes and backslashes
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'{key} = "{escaped_value}"\n')

    print(f'Updated {file_path}')

print(f"\nCompleted footer translation for {len(translations)} languages")
