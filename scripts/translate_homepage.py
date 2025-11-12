#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# All the hardcoded strings in the homepage layout
layout_strings = {
    "heroTitle": "Welcome to the Invisible Internet",
    "heroDescription": "I2P (Invisible Internet Project) is a decentralized, privacy-focused network that allows people to communicate and share information anonymously. It works by routing data through multiple encrypted layers across volunteer-operated nodes, hiding both the sender's and receiver's locations. The result is a secure, censorship-resistant network designed for private websites, messaging, and data sharing.",
    "downloadI2P": "Download I2P",

    # Stats labels
    "yearsActive": "Years Active",
    "activeRouters": "Active Routers",
    "openSource": "Open Source",

    # Latest Updates section
    "latestUpdates": "Latest Updates",
    "moreBlogPosts": "More blog posts →",

    # Features section
    "i2pFeatures": "I2P Features",

    # Feature 1
    "endToEndEncrypted": "End-to-End Encrypted",
    "endToEndEncryptedDesc": "All traffic is encrypted multiple times through distributed routers.",

    # Feature 2
    "anonymousByDefault": "Anonymous by Default",
    "anonymousByDefaultDesc": "Your IP and identity are hidden from the network itself.",

    # Feature 3
    "censorshipResistant": "Censorship Resistant",
    "censorshipResistantDesc": "Decentralized architecture makes blocking extremely difficult.",

    # Feature 4
    "communityDriven": "Community Driven",
    "communityDrivenDesc": "Open source and maintained by volunteers worldwide.",

    # Feature 5
    "fullyDistributed": "Fully Distributed",
    "fullyDistributedDesc": "No central servers or points of failure.",

    # Feature 6
    "selfContainedNetwork": "Self-Contained Network",
    "selfContainedNetworkDesc": "Complete ecosystem for private communication.",
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
    for string_key, string_value in layout_strings.items():
        batch_requests.append({
            "custom_id": f"homepage_{lang_code}_{string_key}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator specializing in technical and privacy-focused content. Translate the following text to {lang_name}. Only output the translation, nothing else. Keep technical terms like 'I2P' unchanged."
                    },
                    {
                        "role": "user",
                        "content": string_value
                    }
                ],
                "max_tokens": 300
            }
        })

print(f"Total strings: {len(layout_strings)}")
print(f"Total languages: {len(languages)}")
print(f"Total requests: {len(batch_requests)}")

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/homepage.jsonl'
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
    metadata={"description": "I2P homepage layout i18n"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/homepage_batch_id.txt', 'w') as f:
    f.write(batch.id)
