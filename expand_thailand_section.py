"""
Update Thailand section with architecture/built environment AI resources
Focused on: AI Strategy, Smart Cities, BIM/Construction AI, and Ethics
"""

import os
import json
from supabase import create_client, Client

# Supabase configuration
url = "https://xcctqbamimafkkamuwly.supabase.co"
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

# Thailand items focused on architecture/built environment AI
thailand_items = [
    {
        "name": "Thailand AI Strategy & Policy Background",
        "url": "https://asiasociety.org/policy-institute/raising-standards-data-ai-southeast-asia/ai/thailand",
        "desc": "Comprehensive overview of Thailand's National AI Strategy 2021-2027, Thailand 4.0 framework, and AI ethics guidelines."
    },
    {
        "name": "AI For Thai Platform",
        "url": "https://www.aiforthai.in.th/",
        "desc": "Official NECTEC platform providing AI tools, services, and demos for Thai developers with 'AI for Everyone' initiative."
    },
    {
        "name": "ASEAN Smart Cities Network",
        "url": "https://asean.org/book/asean-smart-cities-network/",
        "desc": "Collaborative platform for smart city development with Thailand's Bangkok, Phuket, Chiang Mai, and Khon Kaen cities."
    },
    {
        "name": "BIM & Construction AI Research",
        "url": "https://www.sciencedirect.com/search?qs=thailand%20construction%20AI%20BIM",
        "desc": "Academic research on BIM integration with AI and IoT for sustainable construction and smart building design in Thailand."
    },
    {
        "name": "Construction 4.0 & Sustainability",
        "url": "https://www.mdpi.com/search?q=thailand+AI+architecture+construction",
        "desc": "Research on Construction 4.0 technologies, digital transformation, and sustainable building practices in Thailand."
    },
    {
        "name": "Thailand Digital Transformation (OECD)",
        "url": "https://www.oecd.org/countries/thailand/",
        "desc": "OECD analysis of Thailand's digital economy, smart infrastructure, and technology adoption in urban development."
    }
]

def update_thailand_section():
    print("Fetching current winners_payload for year 2026...")
    
    # Fetch current data
    response = supabase.table("winners_payload").select("*").eq("year", 2026).execute()
    
    if not response.data or len(response.data) == 0:
        print("Error: No data found for year 2026")
        return
    
    current_data = response.data[0]
    payload = current_data["payload"]
    
    # Find Thailand category (should be index 2 in categories)
    thailand_idx = None
    for idx, category in enumerate(payload["sections"][0]["categories"]):
        if category.get("subtitle") == "Thailand":
            thailand_idx = idx
            break
    
    if thailand_idx is None:
        print("Error: Thailand category not found")
        return
    
    old_count = len(payload["sections"][0]["categories"][thailand_idx]["items"])
    
    # Update Thailand items
    payload["sections"][0]["categories"][thailand_idx]["items"] = thailand_items
    
    # Update in database
    print(f"\nUpdated Thailand items:")
    print(f"  Old count: {old_count}")
    print(f"  New count: {len(thailand_items)} ({len(thailand_items)} items)")
    print(f"  Focus: AI Strategy, Smart Cities, BIM/Construction, Digital Transformation")
    print("\nUpdating database...")
    
    update_response = supabase.table("winners_payload").update({
        "payload": payload
    }).eq("year", 2026).execute()
    
    if update_response.data:
        print("✓ Successfully updated Thailand section for architecture/built environment AI")
        print(f"✓ Thailand now has {len(thailand_items)} curated resources")
        print("✓ Covers: National AI Strategy, Smart Cities, BIM, Construction 4.0, Digital Transformation")
    else:
        print("Error updating database")

if __name__ == "__main__":
    update_thailand_section()
