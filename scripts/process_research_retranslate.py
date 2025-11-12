#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/research_retranslate_batch_id.txt') as f:
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

# Parse results and write files
for line in results:
    data = json.loads(line)
    custom_id = data['custom_id']
    lang_code = custom_id.replace('research_', '')

    if data['response']['status_code'] == 200:
        translated_content = data['response']['body']['choices'][0]['message']['content']

        # Write to file
        output_path = f'/Users/dustinfields/git/i2p.www/content/{lang_code}/research.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f'Updated {output_path}')
    else:
        print(f'Error translating {lang_code}: {data["response"]["status_code"]}')

print("\nCompleted research page retranslation")
