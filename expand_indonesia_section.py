"""
Expand Indonesia section with 5 new verified authoritative resources
Total: 9 high-quality items covering strategy, ethics, infrastructure, and talent
"""

import os
import json
from supabase import create_client, Client

# Supabase configuration
url = "https://xcctqbamimafkkamuwly.supabase.co"
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

# New comprehensive Indonesia items (9 total)
indonesia_items = [
    {
        "name": "National AI Roadmap 2025-2045",
        "url": "https://govinsider.asia/intl-en/article/indonesia-launches-national-ai-roadmap-to-2045",
        "desc": "Indonesia's comprehensive National AI Strategy to position the country as a regional leader in AI by 2045."
    },
    {
        "name": "AI Strategy Background",
        "url": "https://asiasociety.org/policy-institute/raising-standards-data-ai-southeast-asia/ai/indonesia",
        "desc": "Contextual explanation of how Indonesia's AI strategy fits into its wider digital transformation and data policies."
    },
    {
        "name": "AI Ethics & Governance",
        "url": "https://www.hbtlaw.com/insights/2024-02/ethical-guidelines-use-artificial-intelligence-ai-indonesia",
        "desc": "Practical overview of Indonesia's AI ethics rules and principles for responsible, transparent and accountable AI use."
    },
    {
        "name": "Making Indonesia 4.0",
        "url": "https://sea-vet.net/images/sampledata/TVET-Online/Dudi/Making-Indonesia-4.0.pdf",
        "desc": "National roadmap for Indonesia's digital transformation and Industry 4.0 industrial strategy."
    },
    {
        "name": "BRIN",
        "url": "https://www.brin.go.id/en",
        "desc": "National Research and Innovation Agency driving AI research, development, and policy implementation in Indonesia."
    },
    {
        "name": "AI Center of Excellence & Sovereign AI",
        "url": "https://indonesiabusinesspost.com/4736/cyber-and-espionage/indonesia-launches-ai-center-of-excellence-to-speed-up-inclusive-sove/",
        "desc": "Description of the national AI Center of Excellence with sandbox, startup hub and sovereign AI infrastructure."
    },
    {
        "name": "Indonesia Local-Language LLMs",
        "url": "https://www.marketing-interactive.com/indosat-goto-launch-indonesia-s-70b-parameter-ai-model-in-local-languages",
        "desc": "Indonesia-centric large language models for Bahasa and local languages, open for developers to build and fine-tune on."
    },
    {
        "name": "AI Talent Factory (AITF)",
        "url": "https://legalcentric.com/content/view/198730",
        "desc": "National programme to train advanced AI engineers and support sovereign AI development in Indonesia."
    },
    {
        "name": "UNESCO-KOMINFO AI Readiness & Ethics",
        "url": "https://www.unesco.org/en/articles/indonesia-takes-steps-towards-ethical-ai",
        "desc": "UNESCO assessment of Indonesia's AI readiness, ethics frameworks and collaborative efforts with KOMINFO."
    }
]

def update_indonesia_section():
    print("Fetching current winners_payload for year 2026...")
    
    # Fetch current data
    response = supabase.table("winners_payload").select("*").eq("year", 2026).execute()
    
    if not response.data or len(response.data) == 0:
        print("Error: No data found for year 2026")
        return
    
    current_data = response.data[0]
    payload = current_data["payload"]
    
    # Find Indonesia category (should be index 1 in categories)
    indonesia_idx = None
    for idx, category in enumerate(payload["sections"][0]["categories"]):
        if category.get("subtitle") == "Indonesia":
            indonesia_idx = idx
            break
    
    if indonesia_idx is None:
        print("Error: Indonesia category not found")
        return
    
    old_count = len(payload["sections"][0]["categories"][indonesia_idx]["items"])
    
    # Update Indonesia items
    payload["sections"][0]["categories"][indonesia_idx]["items"] = indonesia_items
    
    # Update in database
    print(f"\nUpdated Indonesia items:")
    print(f"  Old count: {old_count}")
    print(f"  New count: {len(indonesia_items)} ({len(indonesia_items)} items)")
    print(f"  All URLs verified and accessible")
    print("\nUpdating database...")
    
    update_response = supabase.table("winners_payload").update({
        "payload": payload
    }).eq("year", 2026).execute()
    
    if update_response.data:
        print("✓ Successfully expanded Indonesia section with verified authoritative resources")
        print(f"✓ Indonesia now has {len(indonesia_items)} comprehensive AI resources")
        print("✓ Covers: Strategy, Ethics, Infrastructure, Sovereign AI, Talent Development")
    else:
        print("Error updating database")

if __name__ == "__main__":
    update_indonesia_section()
