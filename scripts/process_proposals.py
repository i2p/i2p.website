#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/proposals_batch_id.txt') as f:
    batch_id = f.read().strip()

# Get batch status
batch = client.batches.retrieve(batch_id)
print(f"Batch status: {batch.status}")

if batch.status != 'completed':
    print(f"Batch not completed yet. Current status: {batch.status}")
    exit(1)

# Load file mapping
with open('/Users/dustinfields/git/i2p.www/scripts/proposals_files.json') as f:
    proposal_files = json.load(f)

# Download results
result_file_id = batch.output_file_id
result = client.files.content(result_file_id)
results = result.text.strip().split('\n')

# Parse results
translations = {}

for line in results:
    data = json.loads(line)
    custom_id = data['custom_id']

    # Parse custom_id: {lang}_proposals_{filename_sanitized}
    parts = custom_id.split('_proposals_', 1)
    lang_code = parts[0]
    file_id = parts[1]

    if data['response']['status_code'] == 200:
        translated_content = data['response']['body']['choices'][0]['message']['content']

        # Find the original filename
        original_filename = None
        for filename in proposal_files:
            sanitized = filename.replace('.md', '').replace('-', '_')
            if sanitized == file_id:
                original_filename = filename
                break

        if original_filename:
            # Create directory if it doesn't exist
            output_dir = f'/Users/dustinfields/git/i2p.www/content/{lang_code}/proposals'
            os.makedirs(output_dir, exist_ok=True)

            # Write the translated file
            output_path = os.path.join(output_dir, original_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
                if not translated_content.endswith('\n'):
                    f.write('\n')

            print(f'Updated {output_path}')
        else:
            print(f'Warning: Could not find original filename for {file_id}')
    else:
        print(f'Error translating {custom_id}: {data["response"]["status_code"]}')

print(f"\nCompleted proposals translation")
