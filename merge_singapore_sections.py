import os
from supabase import create_client, Client

# Initialize Supabase client
url = "https://xcctqbamimafkkamuwly.supabase.co"
key = os.environ.get('SUPABASE_SERVICE_KEY')

if not key:
    print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
    exit(1)

supabase: Client = create_client(url, key)

# Define the comprehensive merged Singapore AI section with all 12 items
merged_singapore_section = {
    "title": "1. AI Framework & Strategy (Singapore)",
    "categories": [
        {
            "subtitle": "Governance & Policy",
            "items": [
                {
                    "name": "AI Verify Foundation",
                    "url": "https://aiverifyfoundation.sg/",
                    "desc": "World's first testing toolkit for AI ethics (11 principles), embedded in NAIS trusted environment and public procurement"
                },
                {
                    "name": "Model AI Governance Framework",
                    "url": "https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework",
                    "desc": "PDPC guidelines for ethical AI deployment, foundational to both NAIS 2019 and 2.0 governance pillars"
                },
                {
                    "name": "AI Singapore",
                    "url": "https://aisingapore.org",
                    "desc": "Flagship NAIS programme for AI R&D, talent development (15k practitioners goal) and practical use cases across sectors"
                },
                {
                    "name": "Enterprise Compute Initiative",
                    "url": "https://www.imda.gov.sg/how-we-can-help/national-ai-strategy/enterprise-compute-initiative",
                    "desc": "NAIS 2.0 infrastructure providing compute, data access and tools to accelerate industry AI projects"
                },
                {
                    "name": "Personal Data Protection Act (PDPA)",
                    "url": "https://www.pdpc.gov.sg/overview-of-pdpa/the-legislation/personal-data-protection-act",
                    "desc": "Singapore's data protection law with provisions for AI systems that process personal data"
                },
                {
                    "name": "Advisory Guidelines on Use of Personal Data in AI Systems",
                    "url": "https://www.pdpc.gov.sg/help-and-resources/2020/01/advisory-guidelines-on-use-of-personal-data-in-ai-recommendation-and-decision-systems",
                    "desc": "PDPC practical advice on managing personal data protection issues in AI recommendation and decision systems"
                },
                {
                    "name": "Compendium of Use Cases",
                    "url": "https://aiverifyfoundation.sg/downloads/Compendium_of_Use_Cases_2nd_Edition.pdf",
                    "desc": "Real-world case studies demonstrating implementation of the Model AI Governance Framework across industries"
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
                    "name": "National Multimodal LLM Programme",
                    "url": "https://www.aisingapore.org/innovation/national-llm/",
                    "desc": "S$70M NAIS 2.0 initiative building Singapore-centric LLMs like MERaLiON with local context, talent and governance guardrails"
                },
                {
                    "name": "AI for Everyone",
                    "url": "https://www.imda.gov.sg/how-we-can-help/skills-and-training/ai-for-everyone",
                    "desc": "National programme to build AI literacy among Singaporeans, helping citizens understand AI basics and use AI tools in daily life and work"
                },
                {
                    "name": "AI for Industry",
                    "url": "https://www.aisingapore.org/innovation/ai-products-services/",
                    "desc": "Programme supporting Singapore businesses to adopt AI solutions through funding, technical expertise and partnerships with AI researchers"
                }
            ]
        }
    ]
}

# Fetch current payload
print("Fetching current winners_payload for year 2026...")
response = supabase.table('winners_payload').select('*').eq('year', 2026).execute()

if not response.data or len(response.data) == 0:
    print("ERROR: No data found for year 2026")
    exit(1)

current_payload = response.data[0]['payload']
current_sections = current_payload.get('sections', [])

print(f"Current sections count: {len(current_sections)}\n")

# Find and replace/update Singapore AI section
singapore_index = None
for idx, section in enumerate(current_sections):
    if "AI Framework & Strategy (Singapore)" in section.get('title', ''):
        singapore_index = idx
        print(f"Found Singapore AI section at index {idx}")
        break

if singapore_index is not None:
    # Replace the existing section with merged version
    current_sections[singapore_index] = merged_singapore_section
    print(f"Replaced section at index {singapore_index} with merged 12-item section")
else:
    # Insert at beginning if not found
    current_sections.insert(0, merged_singapore_section)
    print("Inserted merged Singapore AI section at beginning")

# Count items
total_items = sum(len(cat.get('items', [])) for cat in merged_singapore_section.get('categories', []))
print(f"\nMerged section has {total_items} total items:")
for cat in merged_singapore_section.get('categories', []):
    cat_title = cat.get('title')
    cat_items = len(cat.get('items', []))
    print(f"  - {cat_title}: {cat_items} items")

# Update the database
print("\nUpdating database...")
update_response = supabase.table('winners_payload').update({
    'payload': {'sections': current_sections}
}).eq('year', 2026).execute()

print("✓ Successfully updated winners_payload with merged Singapore AI section")
print(f"✓ Total sections: {len(current_sections)}")
print(f"✓ Singapore AI section now has 12 items across 2 categories")
