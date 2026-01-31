#!/usr/bin/env python3
"""
Add Singapore AI Framework & Strategy section to winners_payload year=2026
for display on public resources.html page
"""
import os
import json
from supabase import create_client, Client

# Load Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("Fetching current winners_payload for year=2026...")
try:
    result = supabase.table('winners_payload').select('*').eq('year', 2026).execute()
    
    if not result.data:
        print("❌ No year=2026 entry found in winners_payload table!")
        exit(1)
    
    current_row = result.data[0]
    payload = current_row.get('payload', {})
    sections = payload.get('sections', [])
    
    print(f"✅ Found year=2026 with {len(sections)} existing sections")
    
    # Create new Singapore AI section
    sg_ai_section = {
        "title": "1. AI Framework & Strategy (Singapore)",
        "categories": [
            {
                "subtitle": "Governance & Policy",
                "items": [
                    {
                        "name": "AI Verify",
                        "url": "https://aiverifyfoundation.sg/",
                        "desc": "World's first testing toolkit for AI ethics (11 principles), embedded in NAIS trusted environment and public procurement"
                    },
                    {
                        "name": "Model AI Governance Framework",
                        "url": "https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework",
                        "desc": "PDPC guidelines for ethical AI deployment, foundational to both NAIS 2019 and 2.0 governance pillars"
                    }
                ]
            },
            {
                "subtitle": "National Strategy & Programmes",
                "items": [
                    {
                        "name": "National AI Strategy 2019",
                        "url": "https://www.smartnation.gov.sg/nais/",
                        "desc": "Original NAIS document unveiled in 2019, outlining five National AI Projects (transport/logistics, smart cities, healthcare, education, security) plus ecosystem enablers like talent, data architecture and triple-helix partnerships"
                    },
                    {
                        "name": "National AI Strategy 2.0",
                        "url": "https://www.smartnation.gov.sg/nais/national-ai-strategy-2/",
                        "desc": "Updated 2023 strategy with 15 actions, SGD 1B+ investment, focusing on AI hubs, compute access, trusted governance and 15,000 AI talents"
                    },
                    {
                        "name": "AI Singapore",
                        "url": "https://aisingapore.org/",
                        "desc": "Flagship NAIS programme for AI R&D, talent development (15k practitioners goal) and practical use cases across sectors"
                    },
                    {
                        "name": "National Multimodal LLM Programme",
                        "url": "https://www.aisingapore.org/innovation/national-llm/",
                        "desc": "S$70M NAIS 2.0 initiative building Singapore-centric LLMs like MERaLiON with local context, talent and governance guardrails"
                    },
                    {
                        "name": "Enterprise Compute Initiative",
                        "url": "https://www.imda.gov.sg/how-we-can-help/national-ai-strategy/enterprise-compute-initiative",
                        "desc": "NAIS 2.0 infrastructure providing compute, data access and tools to accelerate industry AI projects"
                    }
                ]
            }
        ]
    }
    
    # Insert at the beginning of sections array
    sections.insert(0, sg_ai_section)
    
    # Renumber existing sections (2., 3., 4., etc.)
    for i, section in enumerate(sections[1:], start=2):
        if 'title' in section:
            # Remove old number prefix if exists
            title = section['title']
            if '. ' in title:
                title = title.split('. ', 1)[1]
            section['title'] = f"{i}. {title}"
    
    # Update payload
    payload['sections'] = sections
    
    # Update database
    print(f"\nUpdating winners_payload year=2026 with {len(sections)} sections...")
    update_result = supabase.table('winners_payload').update({
        'payload': payload
    }).eq('year', 2026).execute()
    
    print(f"✅ Successfully updated year=2026!")
    print(f"\nNew section added:")
    print(f"  1. AI Framework & Strategy (Singapore)")
    print(f"     - Governance & Policy: 2 resources")
    print(f"     - National Strategy & Programmes: 5 resources")
    print(f"\nTotal sections now: {len(sections)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n✅ Done! Singapore AI resources will now appear on https://aihackathon.pro/resources.html")
