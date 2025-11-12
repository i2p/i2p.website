#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/get_involved_batch_id.txt') as f:
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

# File mapping
file_mapping = {
    'get-involved__index': 'get-involved/_index.md',
    'get-involved_roadmap': 'get-involved/roadmap.md',
    'get-involved_guides_translator-guide': 'get-involved/guides/translator-guide.md'
}

# Parse results
for line in results:
    data = json.loads(line)
    custom_id = data['custom_id']

    # Extract language code and file identifier
    parts = custom_id.split('_', 1)
    lang_code = parts[0]
    file_id = parts[1]

    if data['response']['status_code'] == 200:
        translated_content = data['response']['body']['choices'][0]['message']['content']

        # Get the file path
        if file_id in file_mapping:
            file_path = file_mapping[file_id]
            output_path = f'/Users/dustinfields/git/i2p.www/content/{lang_code}/{file_path}'

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Write the translated file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
                if not translated_content.endswith('\n'):
                    f.write('\n')

            print(f'Updated {output_path}')
        else:
            print(f'Warning: Unknown file_id {file_id}')
    else:
        print(f'Error translating {custom_id}: {data["response"]["status_code"]}')

print(f"\nCompleted get-involved translation")
