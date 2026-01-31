#!/usr/bin/env python3
"""
Update and add Singapore AI Framework & Strategy resources to Supabase members_resources table
Based on existing entries visible in the screenshot:
- ID 1: AI Singapore (update)
- ID 2: AI Verify (update)
- ID 3: Model AI Governance Framework (update)
- ID 5: Enterprise Compute Initiative (update)
New entries to add:
- National AI Strategy 2019
- National AI Strategy 2.0
- National Multimodal LLM Programme
"""
import os
from supabase import create_client, Client

# Load Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    print("Please set it using:")
    print("  $env:SUPABASE_SERVICE_KEY='your-service-key-here'")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Update existing entries
updates = [
    {
        'id': 1,
        'title': 'AI Framework & Strategy (Singapore) - AI Singapore',
        'url': 'https://aisingapore.org/',
        'note': 'Flagship NAIS programme for AI R&D, talent development (15k practitioners goal) and practical use cases across sectors.'
    },
    {
        'id': 2,
        'title': 'AI Framework & Strategy (Singapore) - AI Verify',
        'url': 'https://aiverifyfoundation.sg/',
        'note': "World's first testing toolkit for AI ethics (11 principles), embedded in NAIS trusted environment and public procurement."
    },
    {
        'id': 3,
        'title': 'AI Framework & Strategy (Singapore) - Model AI Governance Framework',
        'url': 'https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework',
        'note': 'PDPC guidelines for ethical AI deployment, foundational to both NAIS 2019 and 2.0 governance pillars.'
    },
    {
        'id': 5,
        'title': 'AI Framework & Strategy (Singapore) - Enterprise Compute Initiative',
        'url': 'https://www.imda.gov.sg/how-we-can-help/national-ai-strategy/enterprise-compute-initiative',
        'note': 'NAIS 2.0 infrastructure providing compute, data access and tools to accelerate industry AI projects.'
    }
]

print("Updating existing AI Framework & Strategy resources...")
for update in updates:
    try:
        result = supabase.table('members_resources').update({
            'title': update['title'],
            'url': update['url'],
            'note': update['note']
        }).eq('id', update['id']).execute()
        print(f"  ✅ Updated ID {update['id']}: {update['title']}")
    except Exception as e:
        print(f"  ❌ Error updating ID {update['id']}: {e}")

# New resources to add
new_resources = [
    {
        'title': 'AI Framework & Strategy (Singapore) - National AI Strategy 2019',
        'url': 'https://www.smartnation.gov.sg/nais/',
        'note': 'Original NAIS document unveiled in 2019, outlining five National AI Projects (transport/logistics, smart cities, healthcare, education, security) plus ecosystem enablers like talent, data architecture and triple-helix partnerships.',
        'sort_order': 19,
        'active': True
    },
    {
        'title': 'AI Framework & Strategy (Singapore) - National AI Strategy 2.0',
        'url': 'https://www.smartnation.gov.sg/nais/national-ai-strategy-2/',
        'note': 'Updated 2023 strategy with 15 actions, SGD 1B+ investment, focusing on AI hubs, compute access, trusted governance and 15,000 AI talents.',
        'sort_order': 20,
        'active': True
    },
    {
        'title': 'AI Framework & Strategy (Singapore) - National Multimodal LLM Programme',
        'url': 'https://www.aisingapore.org/innovation/national-llm/',
        'note': 'S$70M NAIS 2.0 initiative building Singapore-centric LLMs like MERaLiON with local context, talent and governance guardrails.',
        'sort_order': 21,
        'active': True
    }
]

print(f"\nAdding {len(new_resources)} new Singapore AI resources...")
try:
    result = supabase.table('members_resources').insert(new_resources).execute()
    print(f"✅ Successfully added {len(new_resources)} new resources!")
    for resource in new_resources:
        print(f"  - {resource['title']}")
        print(f"    {resource['url']}")
except Exception as e:
    print(f"❌ Error inserting resources: {e}")
    exit(1)

print("\n✅ Done! Updated 4 existing resources and added 3 new resources to members_resources table.")
