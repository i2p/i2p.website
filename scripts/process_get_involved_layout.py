#!/usr/bin/env python3
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Read batch ID
with open('/Users/dustinfields/git/i2p.www/scripts/get_involved_layout_batch_id.txt') as f:
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

    # Parse custom_id: getinvolved_{lang}_{key}
    parts = custom_id.replace('getinvolved_', '').split('_', 1)
    lang_code = parts[0]
    string_key = parts[1]

    if data['response']['status_code'] == 200:
        translated_text = data['response']['body']['choices'][0]['message']['content']

        if lang_code not in translations:
            translations[lang_code] = {}

        translations[lang_code][string_key] = translated_text

# Add English strings
translations['en'] = {
    "heroTitle": "Get Involved with I2P",
    "heroDescription": "Join our community and help build a more private, secure internet for everyone. Whether you're a developer, translator, researcher, or enthusiast, there's a place for you.",
    "coreDevelopment": "Core Development",
    "coreDevelopmentDesc": "Contribute to the I2P codebase. Fix bugs, add features, and help improve performance for thousands of users worldwide.",
    "newDeveloperGuide": "New Developer Guide",
    "browseSourceCode": "Browse Source Code",
    "proposals": "Proposals",
    "buildApplications": "Build Applications",
    "buildApplicationsDesc": "Create applications that run on I2P. From chat apps to file sharing, your apps can help expand the I2P ecosystem.",
    "apiDocumentation": "API Documentation",
    "newRouterGuide": "New Router Guide",
    "hostInfrastructure": "Host Infrastructure",
    "hostInfrastructureDesc": "Help new users join the network by running reseed servers, mirrors, and other critical infrastructure services.",
    "reseedDocumentation": "Reseed Documentation",
    "mirrorSetupGuide": "Mirror Setup Guide",
    "serviceHosting": "Service Hosting",
    "documentation": "Documentation",
    "documentationDesc": "Help others understand I2P by writing guides, updating documentation, and creating tutorials.",
    "documentationHub": "Documentation Hub",
    "writingGuidelines": "Writing Guidelines",
    "contentSuggestions": "Content Suggestions",
    "translation": "Translation",
    "translationDesc": "Make I2P accessible to more people by translating the website, software interface, and documentation.",
    "translatorsGuide": "Translator's Guide",
    "translationPlatform": "Translation Platform",
    "languageStatus": "Language Status",
    "researchSecurity": "Research & Security",
    "researchSecurityDesc": "Analyze the codebase, conduct security research, and help make I2P more robust and secure.",
    "vulnerabilityReporting": "Vulnerability Reporting",
    "researchTopics": "Research Topics",
    "researchPapers": "Research Papers",
    "communitySupport": "Community Support",
    "communitySupportDesc": "Help others by answering questions, participating in forums, and spreading the word about I2P.",
    "officialForums": "Official Forums",
    "redditCommunity": "Reddit Community",
    "ircChannels": "IRC Channels",
    "runRouter": "Run a Router",
    "runRouterDesc": "Simply running an I2P router helps strengthen the network. Every participant makes I2P more resilient.",
    "downloadI2P": "Download I2P",
    "gettingStarted": "Getting Started",
    "routerConfiguration": "Router Configuration",
    "financialSupport": "Financial Support",
    "financialSupportDesc": "Support I2P development and infrastructure costs through donations and sponsorships.",
    "donate": "Donate",
    "sponsorDevelopment": "Sponsor Development",
    "corporateSupport": "Corporate Support",
    "ctaTitle": "Ready to Get Started?",
    "ctaDescription": "Join the I2P community today and help build a more private and secure internet. Every contribution, no matter how small, makes a difference.",
    "contactUs": "Contact Us"
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

    # Append getInvolved section
    with open(file_path, 'a', encoding='utf-8') as f:
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write('\n[getInvolved]\n')
        for key, value in strings.items():
            # Escape quotes and backslashes
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'{key} = "{escaped_value}"\n')

    print(f'Updated {file_path}')

print(f"\nCompleted get-involved layout translation for {len(translations)} languages")
