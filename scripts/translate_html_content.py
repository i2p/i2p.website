#!/usr/bin/env python3
"""
Translate HTML content files using OpenAI Batch API.

This script:
1. Parses HTML files to extract translatable text
2. Preserves HTML structure and attributes
3. Doesn't translate: author names, BibTeX, URLs, code
4. Translates: headings, paragraphs, buttons, links text
"""
import os
import json
import re
from pathlib import Path
from openai import OpenAI

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    print("Error: beautifulsoup4 not installed. Run: pip install beautifulsoup4")
    exit(1)

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Elements that contain translatable text
TRANSLATABLE_ELEMENTS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'button', 'span', 'div'}

# Classes/IDs that indicate non-translatable content
NON_TRANSLATABLE_CLASSES = {'bibtex-content', 'paper-authors', 'code', 'language-'}
NON_TRANSLATABLE_IDS = {'bibtex', 'code'}

def should_translate_element(element):
    """Determine if an element's text should be translated."""
    if not isinstance(element, Tag):
        return False

    # Check for non-translatable classes
    if element.get('class'):
        classes = ' '.join(element.get('class'))
        for non_trans in NON_TRANSLATABLE_CLASSES:
            if non_trans in classes:
                return False

    # Check for non-translatable IDs
    if element.get('id'):
        elem_id = element.get('id')
        for non_trans in NON_TRANSLATABLE_IDS:
            if non_trans in elem_id:
                return False

    # Don't translate if it's just a year number
    text = element.get_text(strip=True)
    if re.match(r'^\d{4}$', text):
        return False

    # Don't translate BibTeX toggles and PDF links separately
    # (we'll handle these with specific rules)

    return True


def extract_translatable_segments(html_content, source_file):
    """Extract translatable text segments from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    segments = []
    segment_id = 0

    # Find all elements with translatable text
    for element in soup.find_all(TRANSLATABLE_ELEMENTS):
        if not should_translate_element(element):
            continue

        # Get direct text content (not from children)
        direct_text = ''.join([
            str(s) for s in element.contents
            if isinstance(s, NavigableString) and str(s).strip()
        ])

        if not direct_text.strip():
            # Check if it's a simple element with only text
            if len(list(element.children)) == 1 and isinstance(list(element.children)[0], NavigableString):
                direct_text = element.get_text(strip=True)
            elif element.name in ['button', 'span'] and not element.find_all():
                direct_text = element.get_text(strip=True)
            else:
                continue

        text = direct_text.strip()
        if not text or len(text) < 2:
            continue

        # Skip if it's just "PDF" or "Show BibTeX" - we'll handle these specially
        if text in ['PDF', 'Show BibTeX']:
            segment_id += 1
            segments.append({
                'id': segment_id,
                'text': text,
                'element_type': element.name,
                'element_class': ' '.join(element.get('class', [])),
                'is_ui': True
            })
        else:
            segment_id += 1
            segments.append({
                'id': segment_id,
                'text': text,
                'element_type': element.name,
                'element_class': ' '.join(element.get('class', [])),
                'is_ui': False
            })

    return segments, soup


def create_batch_requests(source_file, target_langs):
    """Create batch translation requests for an HTML file."""
    source_path = Path(source_file)
    html_content = source_path.read_text(encoding='utf-8')

    # Extract front matter
    front_matter = ""
    body_content = html_content
    if html_content.startswith('---'):
        parts = html_content.split('---', 2)
        if len(parts) >= 3:
            front_matter = f"---{parts[1]}---"
            body_content = parts[2]

    segments, soup = extract_translatable_segments(body_content, source_file)

    print(f"\nFound {len(segments)} translatable segments in {source_file}")

    # Preview some segments
    print("\nSample segments:")
    for seg in segments[:5]:
        print(f"  [{seg['id']}] {seg['element_type']}.{seg['element_class']}: {seg['text'][:60]}...")

    requests = []
    file_base = source_path.stem

    for lang_code, lang_name in target_langs.items():
        for segment in segments:
            custom_id = f"html_{file_base}_{lang_code}_seg{segment['id']}"

            # Different prompts for UI elements vs content
            if segment.get('is_ui'):
                user_prompt = f"Translate this UI element to {lang_name}. Keep it very short and concise:\n{segment['text']}"
            else:
                user_prompt = f"Translate the following text to {lang_name}. Preserve any markdown or formatting:\n{segment['text']}"

            requests.append({
                'custom_id': custom_id,
                'method': 'POST',
                'url': '/v1/chat/completions',
                'body': {
                    'model': 'gpt-4o',
                    'messages': [
                        {
                            'role': 'system',
                            'content': f'You are a professional translator. Translate to {lang_name}. Only output the translation. Do NOT translate: author names, technical terms like I2P, URLs, or code.'
                        },
                        {
                            'role': 'user',
                            'content': user_prompt
                        }
                    ],
                    'max_tokens': 500
                }
            })

    return requests, segments, front_matter


def main():
    source_file = '/Users/dustinfields/git/i2p.www/content/en/papers.html'

    target_langs = {
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

    print("Analyzing HTML file...")
    requests, segments, front_matter = create_batch_requests(source_file, target_langs)

    print(f"\nTotal requests: {len(requests)}")
    print(f"Total segments: {len(segments)}")
    print(f"Total languages: {len(target_langs)}")

    # Save segment mapping for reconstruction
    mapping_file = '/Users/dustinfields/git/i2p.www/scripts/papers_segments.json'
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump({
            'segments': segments,
            'front_matter': front_matter,
            'source_file': source_file
        }, f, ensure_ascii=False, indent=2)

    print(f"\nSaved segment mapping to: {mapping_file}")

    # Write batch file
    batch_file = '/Users/dustinfields/git/i2p.www/scripts/batches/papers_html.jsonl'
    os.makedirs(os.path.dirname(batch_file), exist_ok=True)

    with open(batch_file, 'w') as f:
        for req in requests:
            f.write(json.dumps(req) + '\n')

    print(f"Created batch file: {batch_file}")

    # Submit batch
    with open(batch_file, 'rb') as f:
        batch_input_file = client.files.create(file=f, purpose='batch')

    batch = client.batches.create(
        input_file_id=batch_input_file.id,
        endpoint='/v1/chat/completions',
        completion_window='24h',
        metadata={'description': 'I2P papers.html translation'}
    )

    print(f"\nBatch ID: {batch.id}")
    print(f"Status: {batch.status}")

    # Save batch ID
    with open('/Users/dustinfields/git/i2p.www/scripts/papers_html_batch_id.txt', 'w') as f:
        f.write(batch.id)

    print("\nNote: This approach extracts text segments but full reconstruction")
    print("may require manual review for complex HTML structures.")


if __name__ == '__main__':
    main()
