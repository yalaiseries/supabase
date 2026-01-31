"""
Update Section 1: AI Governance, Strategy & Programmes with shortened descriptions
All 4 ASEAN countries: Singapore, Indonesia, Thailand, Malaysia
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

# Section 1: AI Policy & Built Environment Resources in Southeast Asia
governance_categories = [
    {
        "subtitle": "Singapore",
        "items": [
            {
                "name": "National AI Strategy (NAIS)",
                "url": "https://www.smartnation.gov.sg/initiatives/national-ai-strategy/",
                "desc": "National AI roadmap across key sectors."
            },
            {
                "name": "AI Singapore",
                "url": "https://aisingapore.org/",
                "desc": "National AI R&D, industry projects and talent programmes."
            },
            {
                "name": "AI Verify Foundation",
                "url": "https://aiverifyfoundation.sg/",
                "desc": "AI governance testing framework and toolkit."
            },
            {
                "name": "AI & Personal Data Guidelines",
                "url": "https://www.pdpc.gov.sg/guidelines-and-consultation/2024/02/advisory-guidelines-on-use-of-personal-data-in-ai-recommendation-and-decision-systems",
                "desc": "PDPC guidance on AI and personal data."
            },
            {
                "name": "Enterprise Compute Initiative",
                "url": "https://www.disg.gov.sg/enterprise-compute-initiative/",
                "desc": "National compute and tools for AI innovation."
            },
            {
                "name": "BCA digitalisation & AI",
                "url": "https://www.frontier-enterprise.com/how-bca-plans-to-digitise-singapores-built-environment/",
                "desc": "How BCA is digitising Singapore's built environment with AI."
            },
            {
                "name": "BEAMP agentic BIM AI",
                "url": "https://www.beamp.sg/cycle6/ai-driven-bim-classification-and-metadata-structuring-for-sketchup-components",
                "desc": "Project using modular/agentic AI for BIM classification and metadata."
            }
        ]
    },
    {
        "subtitle": "Indonesia",
        "items": [
            {
                "name": "National AI Roadmap 2025–2045",
                "url": "https://govinsider.asia/intl-en/article/indonesia-launches-national-ai-roadmap-to-2045",
                "desc": "Long‑term national AI roadmap."
            },
            {
                "name": "National AI Strategy",
                "url": "https://asiasociety.org/policy-institute/raising-standards-data-ai-southeast-asia/ai/indonesia",
                "desc": "Overview of Indonesia's AI strategy."
            },
            {
                "name": "AI Ethics & Governance",
                "url": "https://www.hbtlaw.com/insights/2024-02/ethical-guidelines-use-artificial-intelligence-ai-indonesia",
                "desc": "AI ethics and governance guidelines."
            },
            {
                "name": "BRIN",
                "url": "https://www.brin.go.id/en",
                "desc": "National research and innovation agency leading AI R&D."
            },
            {
                "name": "Local‑Language LLMs",
                "url": "https://www.marketing-interactive.com/indosat-goto-launch-indonesia-s-70b-parameter-ai-model-in-local-languages",
                "desc": "Bahasa and local‑language LLMs."
            },
            {
                "name": "AI Transforming Building Design & Construction",
                "url": "https://architect.jakartadaily.id/ai-transforming-building-design-construction/",
                "desc": "Use of AI in Indonesia's building design and construction."
            },
            {
                "name": "3D Model AI Reconstruction (Nusantara)",
                "url": "https://ieeexplore.ieee.org/document/10844662/",
                "desc": "AI‑based 3D reconstruction for Nusantara building projects."
            }
        ]
    },
    {
        "subtitle": "Thailand",
        "items": [
            {
                "name": "Thailand AI Strategy & Policy",
                "url": "https://asiasociety.org/policy-institute/raising-standards-data-ai-southeast-asia/ai/thailand",
                "desc": "Overview of Thailand's national AI strategy."
            },
            {
                "name": "AI Thailand Strategy & Action Plan",
                "url": "http://www.ai.in.th/en/about-ai-thailand/",
                "desc": "Official national AI strategy and plan 2022–2027."
            },
            {
                "name": "AI For Thai Platform",
                "url": "https://www.aiforthai.in.th/",
                "desc": "National AI tools, APIs and demos."
            },
            {
                "name": "ASEAN Smart Cities Network",
                "url": "https://asean.org/book/asean-smart-cities-network/",
                "desc": "Smart‑city collaboration including Thai cities."
            },
            {
                "name": "BIM & Construction AI Research",
                "url": "https://www.sciencedirect.com/search?qs=thailand%20construction%20AI%20BIM",
                "desc": "Research on AI and BIM in Thai construction."
            },
            {
                "name": "Construction Tech in Thailand",
                "url": "https://marketresearchthailand.com/insights/articles/how-construction-technology-thailand-is-boosting-the-efficiency",
                "desc": "AI and Construction 4.0 in Thai projects."
            },
            {
                "name": "AI Building Our Future",
                "url": "https://www.nationthailand.com/tech/30347371",
                "desc": "Article on AI and BIM in a major Thai developer's workflow."
            }
        ]
    },
    {
        "subtitle": "Malaysia",
        "items": [
            {
                "name": "National AI Office (NAIO)",
                "url": "https://ai.gov.my/",
                "desc": "National AI coordination office and action plan."
            },
            {
                "name": "SME AI via Open Source",
                "url": "https://ai.gov.my/governance",
                "desc": "Governance and open‑source AI resources for SMEs."
            },
            {
                "name": "National AI Governance & Ethics",
                "url": "https://mastic.mosti.gov.my/publication/the-national-guidelines-on-ai-governance-ethics/",
                "desc": "National AI governance guidelines."
            },
            {
                "name": "MyDIGITAL Initiative",
                "url": "https://mydigital.gov.my/",
                "desc": "Digital economy and AI master plan."
            },
            {
                "name": "MDEC",
                "url": "https://mdec.my/",
                "desc": "Agency supporting Malaysia's digital and AI ecosystem."
            },
            {
                "name": "DBKL AI Digital Twin",
                "url": "https://hiverlab.com/dbkl-ai-and-digital-twin-build-for-smarter-malaysia/",
                "desc": "KL city hall using AI and digital twins for urban management."
            },
            {
                "name": "Future of AI in Malaysian Enterprises",
                "url": "https://www.linkedin.com/pulse/future-ai-malaysian-enterprises-architecture-adoption-david-ho-hdrcc",
                "desc": "Discussion of AI architecture and adoption in Malaysian enterprises."
            }
        ]
    }
]

def update_governance_section():
    """Update Section 1: AI Policy & Built Environment Resources in Southeast Asia"""
    
    print("Fetching current data from Supabase...")
    
    # Fetch the current 2026 winners data
    response = supabase.table("winners_payload").select("*").eq("year", 2026).execute()
    
    if not response.data or len(response.data) == 0:
        print("❌ No 2026 data found")
        return
    
    record = response.data[0]
    payload = record['payload']
    
    # Find Section 1
    section_index = None
    for i, section in enumerate(payload['sections']):
        if '1.' in section['title'] or 'Governance' in section['title'] or 'Policy' in section['title']:
            section_index = i
            break
    
    if section_index is not None:
        # Update existing Section 1
        payload['sections'][section_index]['title'] = '1. AI Policy & Built Environment Resources in Southeast Asia (Sg, In, Th, My)'
        payload['sections'][section_index]['categories'] = governance_categories
        print(f"✅ Updated Section 1: {payload['sections'][section_index]['title']}")
    else:
        # Create new Section 1
        new_section = {
            'title': '1. AI Policy & Built Environment Resources in Southeast Asia (Sg, In, Th, My)',
            'categories': governance_categories
        }
        payload['sections'].insert(0, new_section)
        print("✅ Created new Section 1: AI Policy & Built Environment Resources in Southeast Asia")
    
    # Count total items
    total_items = sum(len(cat['items']) for cat in governance_categories)
    print(f"\nTotal countries: {len(governance_categories)}")
    print(f"Total resources: {total_items}")
    
    # Update the database
    print("\nUpdating database...")
    update_response = supabase.table("winners_payload").update({
        "payload": payload
    }).eq("year", 2026).execute()
    
    if update_response.data:
        print("✅ Database updated successfully!")
        print(f"\nCountries updated:")
        for i, category in enumerate(governance_categories, 1):
            print(f"{i}. {category['subtitle']} ({len(category['items'])} resources)")
    else:
        print("❌ Database update failed")

if __name__ == "__main__":
    update_governance_section()
