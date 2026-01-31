"""
Expand Malaysia section with verified AI governance and strategy resources.
Focus: Built Environment AI Hackathon - Agentic AI, smart buildings, construction AI
"""

import os
import json
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_SERVICE_KEY environment variable not set")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Malaysia AI resources - verified accessible authoritative sources
malaysia_resources = [
    {
        "name": "National AI Office (NAIO)",
        "url": "https://ai.gov.my/",
        "desc": "The central authority driving the 2026–2030 Action Plan focused on safety, security, and digital sovereignty."
    },
    {
        "name": "Accelerating SME AI Adoption Through Open Source",
        "url": "https://ai.gov.my/governance",
        "desc": "NAIO's framework helps SMEs adopt low-cost, ethical AI for automation in construction and public services."
    },
    {
        "name": "National Guidelines on AI Governance and Ethics",
        "url": "https://mastic.mosti.gov.my/publication/the-national-guidelines-on-ai-governance-ethics/",
        "desc": "Seven voluntary principles (fairness, accountability, etc.) specifically targeting responsible use in the built environment."
    },
    {
        "name": "MyDIGITAL Initiative",
        "url": "https://mydigital.gov.my/",
        "desc": "The master plan for 2021–2030, integrating AI into smart cities and intelligent building systems."
    },
    {
        "name": "Malaysia Digital Economy Corporation (MDEC)",
        "url": "https://mdec.my/",
        "desc": "Operates PDTI (talent) and MDAG-AI (funding) to help businesses transition from AI consumers to producers."
    },
    {
        "name": "ASEAN Guide on AI Governance and Ethics",
        "url": "https://asean.org/book/asean-guide-on-ai-governance-and-ethics/",
        "desc": "A regional framework to harmonize cross-border AI standards and smart city development."
    },
    {
        "name": "AI Agents For Every Business",
        "url": "https://www.agenticworkforce.io/ai-agents-malaysia",
        "desc": "Strategic deployment of AI agents to manage business tasks (e.g., e-invoicing, facility management), leveraging Malaysia's 29% AI market CAGR and JS-SEZ tax incentives."
    }
]

def update_malaysia_section():
    """Update the Malaysia section in the database"""
    
    print("Fetching current data from Supabase...")
    
    # Fetch the current 2026 winners data
    response = supabase.table("winners_payload").select("*").eq("year", 2026).execute()
    
    if not response.data or len(response.data) == 0:
        print("❌ No 2026 data found")
        return
    
    record = response.data[0]
    payload = record['payload']
    
    # Find Section 1: AI Governance, Strategy & Programmes
    section = payload['sections'][0]
    print(f"Section: {section['title']}")
    
    # Check current categories (countries)
    current_countries = [cat['subtitle'] for cat in section['categories']]
    print(f"Current countries: {current_countries}")
    
    # Add or update Malaysia category
    malaysia_exists = any(cat['subtitle'] == 'Malaysia' for cat in section['categories'])
    
    if malaysia_exists:
        # Update existing Malaysia category
        for cat in section['categories']:
            if cat['subtitle'] == 'Malaysia':
                cat['items'] = malaysia_resources
                print(f"✅ Updated Malaysia section with {len(malaysia_resources)} resources")
    else:
        # Add new Malaysia category
        malaysia_category = {
            "subtitle": "Malaysia",
            "items": malaysia_resources
        }
        section['categories'].append(malaysia_category)
        print(f"✅ Added new Malaysia section with {len(malaysia_resources)} resources")
    
    # Update the database
    print("\nUpdating database...")
    update_response = supabase.table("winners_payload").update({
        "payload": payload
    }).eq("year", 2026).execute()
    
    if update_response.data:
        print("✅ Database updated successfully!")
        print(f"\nMalaysia resources added:")
        for i, resource in enumerate(malaysia_resources, 1):
            print(f"{i}. {resource['name']}")
            print(f"   URL: {resource['url']}")
    else:
        print("❌ Database update failed")

if __name__ == "__main__":
    update_malaysia_section()
