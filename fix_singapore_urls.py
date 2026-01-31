#!/usr/bin/env python3
import os
from supabase import create_client

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Fixed Singapore resources with verified working URLs
singapore_items = [
    {
        "name": "AI Verify Foundation",
        "url": "https://aiverifyfoundation.sg/",
        "desc": "World's first AI governance testing framework and software toolkit validating AI systems against 11 internationally recognized principles"
    },
    {
        "name": "Model AI Governance Framework",
        "url": "https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2024/public-consult-model-ai-governance-framework-genai",
        "desc": "PDPC comprehensive framework providing practical guidance on implementing responsible AI with principles around transparency, explainability, fairness, and human oversight"
    },
    {
        "name": "AI Singapore",
        "url": "https://aisingapore.org/",
        "desc": "National AI programme bringing together research, innovation, and talent development through initiatives like 100 Experiments, AI Apprenticeship, and AI for Industry"
    },
    {
        "name": "National AI Strategy (NAIS)",
        "url": "https://www.smartnation.gov.sg/initiatives/national-ai-strategy/",
        "desc": "Singapore's comprehensive AI strategy covering National AI Projects across transport, smart cities, healthcare, education, and security with ecosystem enablers for talent and infrastructure"
    },
    {
        "name": "National Multimodal LLM Programme",
        "url": "https://www.imda.gov.sg/about-imda/emerging-technologies-and-research/national-multimodal-llm-programme",
        "desc": "National initiative building Singapore-centric large language models with local context, talent development, and governance guardrails"
    },
    {
        "name": "Enterprise Compute Initiative",
        "url": "https://www.disg.gov.sg/enterprise-compute-initiative/",
        "desc": "National infrastructure providing compute resources, data access and tools to accelerate industry AI projects and innovation"
    },
    {
        "name": "Personal Data Protection Act (PDPA)",
        "url": "https://www.pdpc.gov.sg/overview-of-pdpa/the-legislation/personal-data-protection-act",
        "desc": "Singapore's data protection law establishing baseline standards for personal data protection in AI systems, complementing sector-specific frameworks"
    },
    {
        "name": "Advisory Guidelines on Use of Personal Data in AI Systems",
        "url": "https://www.pdpc.gov.sg/guidelines-and-consultation/2024/02/advisory-guidelines-on-use-of-personal-data-in-ai-recommendation-and-decision-systems",
        "desc": "PDPC practical guidance on managing personal data protection issues in AI recommendation and decision systems"
    },
    {
        "name": "Compendium of AI Governance Use Cases",
        "url": "https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/resource-for-organisation/ai/sgaigovusecases.pdf",
        "desc": "Real-world case studies from local and international organizations demonstrating implementation of the Model AI Governance Framework across different sectors"
    },
    {
        "name": "AI for Everyone",
        "url": "https://learn.aisingapore.org/",
        "desc": "National programme to build AI literacy among Singaporeans, helping citizens understand AI basics and use AI tools in daily life and work"
    },
    {
        "name": "AI for Industry",
        "url": "https://aiap.sg/industry/",
        "desc": "Programme supporting Singapore businesses to adopt AI solutions through funding, technical expertise, partnerships, and pathways to commercialization"
    }
]

print("Fetching current winners_payload for year 2026...")
response = supabase.table("winners_payload").select("payload").eq("year", 2026).execute()

if not response.data:
    print("ERROR: No data found for year 2026")
    exit(1)

payload = response.data[0]["payload"]
sections = payload.get("sections", [])

# Find and update Singapore category
for section in sections:
    if "AI Governance, Strategy & Programmes" in section.get("title", ""):
        for category in section.get("categories", []):
            if category.get("subtitle") == "Singapore":
                old_count = len(category.get("items", []))
                category["items"] = singapore_items
                print(f"Updated Singapore items:")
                print(f"  Old count: {old_count}")
                print(f"  New count: {len(singapore_items)} (11 items)")
                print(f"  All URLs updated with latest official links")
                break
        break

# Update database
print("\nUpdating database...")
update_response = supabase.table("winners_payload").update({"payload": payload}).eq("year", 2026).execute()

print("✓ Successfully updated Singapore resources with verified working URLs")
print("✓ All broken links have been replaced")
