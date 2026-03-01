"""Remove broken links from Section 7"""
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

# Only keep working URLs
section_7_fixed = {
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
                    "name": "Digital Shred",
                    "url": "https://www.digitalshred.com/",
                    "desc": "Digital design teaching materials for architecture/engineering."
                },
                {
                    "name": "GPT in Construction Research",
                    "url": "https://arxiv.org/search/?query=GPT+construction",
                    "desc": "Research PDFs on GPT applications in construction."
                },
                {
                    "name": "IDS Standard",
                    "url": "https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids",
                    "desc": "Information Delivery Specification. (video)"
                },
                {
                    "name": "BCA BIM Standards",
                    "url": "https://www.bca.gov.sg/bim/others/BCA_Model_Content_Requirements_Guide.xlsx",
                    "desc": "BCA Excel template for BIM standards."
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

print(f"Updating section 7 to remove {7} broken links...")
print(f"Keeping {4 + 10} working links\n")

sections[6] = section_7_fixed
payload['sections'] = sections

update_response = requests.patch(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026",
    headers=headers,
    json={"payload": payload, "updated_at": "now()"}
)

if update_response.status_code in [200, 204]:
    print("SUCCESS! Removed broken links from section 7")
    print(f"  Main items: {len(section_7_fixed['categories'][0]['items'])}")
    print(f"  Industry Standards & Tools: {len(section_7_fixed['categories'][1]['items'])}")
    print(f"  Total working links: {len(section_7_fixed['categories'][0]['items']) + len(section_7_fixed['categories'][1]['items'])}")
    print("\nRemoved:")
    print("  - Autodesk on GenAI (403)")
    print("  - GenAI Primer (404)")
    print("  - Intro to GenAI (404)")
    print("  - AI Governance (404)")
    print("  - Bryden Wood (404)")
    print("  - Promx (connection error)")
    print("  - Linked Building Data (403)")
else:
    print(f"Failed: {update_response.status_code}")
    print(update_response.text)
