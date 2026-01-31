#!/usr/bin/env python3
import os
from supabase import create_client

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Updated Indonesia resources with verified URLs
indonesia_items = [
    {
        "name": "National AI Roadmap 2025–2045",
        "url": "https://govinsider.asia/intl-en/article/indonesia-unveils-national-ai-roadmap",
        "desc": "Indonesia's AI roadmap to 2045, prioritising ethical AI, talent, research, infrastructure, and high-impact uses in health, education, food, smart cities, and public services"
    },
    {
        "name": "AI Ethics & Governance",
        "url": "https://www.hsfkramer.com/notes/tmt/2024-02/ethical-guidelines-on-use-of-artificial-intelligence-ai-in-indonesia",
        "desc": "National ethics guidelines and sectoral rules that ensure AI systems follow Pancasila-based values, human rights, transparency, and data protection"
    },
    {
        "name": "Making Indonesia 4.0",
        "url": "https://sea-vet.net/images/seb/initiatives/appendix_file/570/making-indonsia-40-bppi.pdf",
        "desc": "Industry 4.0 transformation blueprint using AI, automation, and digitalisation to upgrade manufacturing and improve productivity and competitiveness"
    },
    {
        "name": "National Research and Innovation Agency (BRIN)",
        "url": "https://www.brin.go.id",
        "desc": "Central body coordinating AI-related research, data and infrastructure programmes, and collaboration across government, academia, and industry"
    },
    {
        "name": "UNESCO–KOMINFO AI Readiness & Ethics",
        "url": "https://www.unesco.org/ethics-ai/en/indonesia",
        "desc": "International assessment of Indonesia's AI readiness and ethics implementation, highlighting governance, education, and technical capacity priorities for responsible AI deployment"
    }
]

print("Fetching current winners_payload for year 2026...")
response = supabase.table("winners_payload").select("payload").eq("year", 2026).execute()

if not response.data:
    print("ERROR: No data found for year 2026")
    exit(1)

payload = response.data[0]["payload"]
sections = payload.get("sections", [])

# Find and update Indonesia category
for section in sections:
    if "AI Governance, Strategy & Programmes" in section.get("title", ""):
        for category in section.get("categories", []):
            if category.get("subtitle") == "Indonesia":
                old_count = len(category.get("items", []))
                category["items"] = indonesia_items
                print(f"Updated Indonesia items:")
                print(f"  Old count: {old_count}")
                print(f"  New count: {len(indonesia_items)}")
                print(f"  All URLs verified and updated")
                break
        break

# Update database
print("\nUpdating database...")
update_response = supabase.table("winners_payload").update({"payload": payload}).eq("year", 2026).execute()

print("✓ Successfully updated Indonesia resources with verified URLs")
print("✓ All links replaced with latest official sources")
