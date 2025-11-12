#!/usr/bin/env python3
"""
Translate papers layout UI strings.
"""
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# All UI strings from papers layout
papers_strings = {
    # Search and filter
    "searchPlaceholder": "Search papers by title, author, or keywords...",
    "filterByYear": "Filter by year:",
    "allYears": "All Years",
    "newestFirst": "Newest First",
    "oldestFirst": "Oldest First",
    "showingPapers": "Showing {visible} of {total} papers",

    # BibTeX
    "showBibtex": "Show BibTeX",
    "hideBibtex": "Hide BibTeX",
    "pdf": "PDF",

    # No results
    "noResultsFound": "No papers found matching your search.",

    # Footer
    "submitEntries": "To submit new or corrected entries:",
    "submitEmail": "Please send to",
    "preferBibtex": "preferably in BibTeX format.",
    "bibSource": "Bibliography source code adapted from the",
    "freeHavenBib": "Free Haven anonymity bibliography",
}

# Languages
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
    for string_key, string_value in papers_strings.items():
        # Special handling for template strings
        if '{visible}' in string_value or '{total}' in string_value:
            prompt = f"Translate to {lang_name}. Keep {{visible}} and {{total}} placeholders unchanged:\n{string_value}"
        else:
            prompt = string_value

        batch_requests.append({
            "custom_id": f"papers_{lang_code}_{string_key}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate to {lang_name}. Only output the translation. Preserve any template placeholders like {{variable}}."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 150
            }
        })

print(f"Total strings: {len(papers_strings)}")
print(f"Total languages: {len(languages)}")
print(f"Total requests: {len(batch_requests)}")

# Write batch file
batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/papers_layout.jsonl'
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
    metadata={"description": "I2P papers layout i18n"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")

# Save batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/papers_layout_batch_id.txt', 'w') as f:
    f.write(batch.id)
