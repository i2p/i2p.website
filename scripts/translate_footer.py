#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# All the hardcoded strings in the footer
footer_strings = {
    # Newsletter section
    "newsletterDescription": "Stay updated with I2P news:",
    "subscribe": "Subscribe",
    "emailPlaceholder": "Enter your email",

    # Quick Links section
    "quickLinks": "Quick Links",
    "donate": "Donate",
    "i2pIntroduction": "I2P Introduction",

    # Community section
    "community": "Community",
    "getInvolved": "Get Involved",
    "blog": "Blog",
    "officialForums": "Official Forums",
    "contact": "Contact",

    # Resources section
    "resources": "Resources",
    "i2pMetrics": "I2P Metrics",
    "research": "Research",
    "gitlab": "GitLab",
    "stormycloud": "StormyCloud",

    # Bottom links
    "copyrightText": "The Invisible Internet Project. Licensed under Creative Commons.",
    "privacy": "Privacy",
    "terms": "Terms",
    "impressum": "Impressum",
    "press": "Press",
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
    for string_key, string_value in footer_strings.items():
        batch_requests.append({
            "custom_id": f"footer_{lang_code}_{string_key}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator specializing in website footer content. Translate the following text to {lang_name}. Keep it concise and natural. Only output the translation, nothing else. Keep technical terms like 'I2P', 'Creative Commons', 'GitLab' unchanged."
                    },
                    {
                        "role": "user",
                        "content": string_value
                    }
                ],
                "max_tokens": 150
            }
        })

print(f"Total strings: {len(footer_strings)}")
print(f"Total languages: {len(languages)}")
print(f"Total requests: {len(batch_requests)}")

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/footer.jsonl'
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
    metadata={"description": "I2P footer i18n"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/footer_batch_id.txt', 'w') as f:
    f.write(batch.id)
