"""Remove the 3 reported non-working links from Section 7"""
import requests
import os

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SERVICE_ROLE_KEY:
    print("Set SERVICE_ROLE_KEY environment variable")
    exit(1)

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Section 7 with the 3 problematic links removed
section_7_cleaned = {
    "title": "7. Education, Standards & Utilities",
    "categories": [
        {
            "items": [
                {
                    "name": "GenAI for Beginners",
                    "url": "https://github.com/microsoft/generative-ai-for-beginners",
                    "desc": "Beginner AI tutorials and code labs on GitHub."
                },
                {
                    "name": "Google Gemini",
                    "url": "https://deepmind.google/technologies/gemini",
                    "desc": "Intro to Google DeepMind's multimodal model family."
                },
                {
                    "name": "AI Agents Explained",
                    "url": "https://www.tech.gov.sg/technews/ai-agents/",
                    "desc": "GovTech explainer on AI agents as digital teammates."
                },
                {
                    "name": "Agentic AI Primer",
                    "url": "https://www.developer.tech.gov.sg/guidelines/standards-and-best-practices/agentic-ai-primer.html",
                    "desc": "GovTech WOG guide for autonomous AI in public sector projects."
                }
            ]
        },
        {
            "name": "Industry Standards & Tools",
            "items": [
                {
                    "name": "Baidu AI",
                    "url": "https://ai.baidu.com/",
                    "desc": "Cloud AI services with vision, NLP, and GenAI APIs."
                },
                {
                    "name": "BCF Standard",
                    "url": "https://www.buildingsmart.org/standards/bsi-standards/bim-collaboration-format-bcf",
                    "desc": "Issue tracking standard. (video)"
                },
                {
                    "name": "Designing Buildings Wiki",
                    "url": "https://www.designingbuildings.co.uk/",
                    "desc": "Community of Practice resource for BIM and construction."
                },
                {
                    "name": "IDS Standard",
                    "url": "https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids",
                    "desc": "Information Delivery Specification. (video)"
                },
                {
                    "name": "Stable Horde",
                    "url": "https://stablehorde.net/",
                    "desc": "Stable Horde distributed GPU network for image generation."
                },
                {
                    "name": "OpenUSD",
                    "url": "https://openusd.org/",
                    "desc": "Universal Scene Description standard. (video)"
                },
                {
                    "name": "BE Industry Digital Plan",
                    "url": "https://services2.imda.gov.sg/ctoaas/builtenvironmentindustrydigitalplan",
                    "desc": "IMDA/BCA guide for BE SMEs adopting AI, DfMA, 3D modelling under PSG grants."
                }
            ]
        }
    ]
}

print("Fetching year 2026 data...")
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026&select=*",
    headers=headers
)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit(1)

rows = response.json()
payload = rows[0]['payload']
sections = payload['sections']

print(f"Removing 3 non-working links from section 7...")
print("  - Digital Shred")
print("  - GPT in Construction Research")
print("  - BCA BIM Standards\n")

sections[6] = section_7_cleaned
payload['sections'] = sections

update_response = requests.patch(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026",
    headers=headers,
    json={"payload": payload, "updated_at": "now()"}
)

if update_response.status_code in [200, 204]:
    print("SUCCESS! Removed 3 non-working links")
    print(f"  Main items: {len(section_7_cleaned['categories'][0]['items'])}")
    print(f"  Industry Standards & Tools: {len(section_7_cleaned['categories'][1]['items'])}")
    print(f"  Total remaining: {len(section_7_cleaned['categories'][0]['items']) + len(section_7_cleaned['categories'][1]['items'])}")
else:
    print(f"Failed: {update_response.status_code}")
    print(update_response.text)
