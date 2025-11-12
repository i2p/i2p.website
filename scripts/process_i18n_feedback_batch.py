#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/i18n_feedback_batch_id.txt') as f:
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
    lang_code = custom_id.split('_')[0]
    string_key = '_'.join(custom_id.split('_')[1:])

    if data['response']['status_code'] == 200:
        translated_text = data['response']['body']['choices'][0]['message']['content']

        if lang_code not in translations:
            translations[lang_code] = {}

        translations[lang_code][string_key] = translated_text

# English strings (original)
translations['en'] = {
    'quickLinks': 'Quick Links',
    'submitFeatureRequest': 'Submit Feature Request',
    'submitFeatureRequestHeading': 'Submit a Feature Request',
    'submitFeatureRequestDesc': 'Have an idea for improving I2P? Share your feature request and vote on existing suggestions.'
}

# Create i18n files
i18n_dir = '/Users/dustinfields/git/i2p.www/i18n'

for lang_code, strings in translations.items():
    file_path = f'{i18n_dir}/{lang_code}.toml'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('[feedback]\n')
        for key, value in strings.items():
            # Escape quotes and backslashes
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'{key} = "{escaped_value}"\n')

    print(f'Created {file_path}')

print(f"\nCreated i18n files for {len(translations)} languages")
