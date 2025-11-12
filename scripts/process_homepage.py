#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/homepage_batch_id.txt') as f:
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

    # Parse custom_id: homepage_{lang}_{key}
    parts = custom_id.replace('homepage_', '').split('_', 1)
    lang_code = parts[0]
    string_key = parts[1]

    if data['response']['status_code'] == 200:
        translated_text = data['response']['body']['choices'][0]['message']['content']

        if lang_code not in translations:
            translations[lang_code] = {}

        translations[lang_code][string_key] = translated_text

# Add English strings
translations['en'] = {
    "heroTitle": "Welcome to the Invisible Internet",
    "heroDescription": "I2P (Invisible Internet Project) is a decentralized, privacy-focused network that allows people to communicate and share information anonymously. It works by routing data through multiple encrypted layers across volunteer-operated nodes, hiding both the sender's and receiver's locations. The result is a secure, censorship-resistant network designed for private websites, messaging, and data sharing.",
    "downloadI2P": "Download I2P",
    "yearsActive": "Years Active",
    "activeRouters": "Active Routers",
    "openSource": "Open Source",
    "latestUpdates": "Latest Updates",
    "moreBlogPosts": "More blog posts →",
    "i2pFeatures": "I2P Features",
    "endToEndEncrypted": "End-to-End Encrypted",
    "endToEndEncryptedDesc": "All traffic is encrypted multiple times through distributed routers.",
    "anonymousByDefault": "Anonymous by Default",
    "anonymousByDefaultDesc": "Your IP and identity are hidden from the network itself.",
    "censorshipResistant": "Censorship Resistant",
    "censorshipResistantDesc": "Decentralized architecture makes blocking extremely difficult.",
    "communityDriven": "Community Driven",
    "communityDrivenDesc": "Open source and maintained by volunteers worldwide.",
    "fullyDistributed": "Fully Distributed",
    "fullyDistributedDesc": "No central servers or points of failure.",
    "selfContainedNetwork": "Self-Contained Network",
    "selfContainedNetworkDesc": "Complete ecosystem for private communication.",
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

    # Append homepage section
    with open(file_path, 'a', encoding='utf-8') as f:
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write('\n[homepage]\n')
        for key, value in strings.items():
            # Escape quotes and backslashes
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'{key} = "{escaped_value}"\n')

    print(f'Updated {file_path}')

print(f"\nCompleted homepage translation for {len(translations)} languages")
