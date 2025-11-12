#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read the English markdown content
with open('/Users/dustinfields/git/i2p.www/content/en/security-response.md', 'r') as f:
    english_content = f.read()

# Layout strings to translate
layout_strings = {
    "securityEmail": "Security Email:",
    "responseTime": "Response Time:",
    "within3Days": "Within 3 working days",
    "quickLinks": "Quick Links",
    "reportVulnerability": "Report Vulnerability",
    "researchGuidelines": "Research Guidelines",
    "responseProcess": "Response Process",
    "researcherCredit": "Researcher Credit",
    "secureCommunication": "Secure Communication",
    "timeline": "Timeline",
    "faq": "FAQ",
    "whatToReport": "What to Report"
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

# Content translation requests
for lang_code, lang_name in languages.items():
    batch_requests.append({
        "custom_id": f"security_content_{lang_code}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a professional translator specializing in security documentation. Translate the following markdown content to {lang_name}. IMPORTANT: Preserve ALL markdown formatting, HTML tags, and front matter exactly. Only translate the text content. Do not add explanations."
                },
                {
                    "role": "user",
                    "content": english_content
                }
            ],
            "max_tokens": 4000
        }
    })

# Layout string translation requests
for lang_code, lang_name in languages.items():
    for string_key, string_value in layout_strings.items():
        batch_requests.append({
            "custom_id": f"security_layout_{lang_code}_{string_key}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following text to {lang_name}. Only output the translation, nothing else."
                    },
                    {
                        "role": "user",
                        "content": string_value
                    }
                ],
                "max_tokens": 100
            }
        })

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/security_all.jsonl'
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
    metadata={"description": "I2P security page full translation"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/security_all_batch_id.txt', 'w') as f:
    f.write(batch.id)
