#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/security_all_batch_id.txt') as f:
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
content_translations = {}
layout_translations = {}

for line in results:
    data = json.loads(line)
    custom_id = data['custom_id']

    if data['response']['status_code'] == 200:
        translated_text = data['response']['body']['choices'][0]['message']['content']

        if custom_id.startswith('security_content_'):
            lang_code = custom_id.replace('security_content_', '')
            content_translations[lang_code] = translated_text
        elif custom_id.startswith('security_layout_'):
            parts = custom_id.replace('security_layout_', '').split('_', 1)
            lang_code = parts[0]
            string_key = parts[1]

            if lang_code not in layout_translations:
                layout_translations[lang_code] = {}

            layout_translations[lang_code][string_key] = translated_text

# Write content files
for lang_code, content in content_translations.items():
    output_path = f'/Users/dustinfields/git/i2p.www/content/{lang_code}/security-response.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {output_path}')

# Add English layout strings
layout_translations['en'] = {
    'securityEmail': 'Security Email:',
    'responseTime': 'Response Time:',
    'within3Days': 'Within 3 working days',
    'quickLinks': 'Quick Links',
    'reportVulnerability': 'Report Vulnerability',
    'researchGuidelines': 'Research Guidelines',
    'responseProcess': 'Response Process',
    'researcherCredit': 'Researcher Credit',
    'secureCommunication': 'Secure Communication',
    'timeline': 'Timeline',
    'faq': 'FAQ',
    'whatToReport': 'What to Report'
}

# Update i18n files
i18n_dir = '/Users/dustinfields/git/i2p.www/i18n'

for lang_code, strings in layout_translations.items():
    file_path = f'{i18n_dir}/{lang_code}.toml'

    # Read existing file if it exists
    existing_content = ''
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # Append security section
    with open(file_path, 'a', encoding='utf-8') as f:
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write('\n[security]\n')
        for key, value in strings.items():
            # Escape quotes and backslashes
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'{key} = "{escaped_value}"\n')

    print(f'Updated i18n {file_path}')

print(f"\nCompleted security page translation for {len(content_translations)} languages")
