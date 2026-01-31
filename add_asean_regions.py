#!/usr/bin/env python3
import os
from supabase import create_client

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Define the new regional section structure
regional_section = {
    "title": "1. AI Governance, Strategy & Programmes",
    "categories": [
        {
            "subtitle": "Singapore",
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
                },
                {
                    "name": "National AI Strategy 2019",
                    "url": "https://www.smartnation.gov.sg/nais/",
                    "desc": "Original NAIS document outlining five National AI Projects (transport/logistics, smart cities, healthcare, education, security) plus ecosystem enablers"
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
                    "desc": "National programme to build AI literacy among Singaporeans, helping citizens understand AI basics and use AI tools in daily life"
                },
                {
                    "name": "AI for Industry",
                    "url": "https://www.aisingapore.org/innovation/ai-products-services/",
                    "desc": "Programme supporting Singapore businesses to adopt AI solutions through funding, technical expertise and partnerships"
                }
            ]
        },
        {
            "subtitle": "Indonesia",
            "items": [
                {
                    "name": "National AI Strategy (Stranas KA)",
                    "url": "https://ai-innovation.id/en/strategi-nasional-kecerdasan-artifisial-indonesia",
                    "desc": "Indonesia's 2020-2045 AI roadmap focusing on ethical AI, talent development, research, and infrastructure across healthcare, education, agriculture, smart cities, and public services"
                },
                {
                    "name": "AI Ethics Guidelines",
                    "url": "https://ai-innovation.id/",
                    "desc": "Framework for responsible AI development in Indonesia, ensuring AI systems align with national values, ethics, and data protection standards"
                },
                {
                    "name": "Making Indonesia 4.0",
                    "url": "https://www.kemenperin.go.id/making-indonesia-4-0",
                    "desc": "Industrial transformation roadmap integrating AI and Industry 4.0 technologies to boost manufacturing competitiveness and economic growth"
                },
                {
                    "name": "National Research and Innovation Agency (BRIN)",
                    "url": "https://www.brin.go.id/",
                    "desc": "Leading Indonesia's AI research, development, and innovation initiatives, coordinating national R&D efforts and AI ecosystem development"
                }
            ]
        },
        {
            "subtitle": "Thailand",
            "items": [
                {
                    "name": "National AI Strategy and Action Plan",
                    "url": "https://www.nstda.or.th/home/ai-policy/",
                    "desc": "Comprehensive strategy aiming to make Thailand ASEAN's AI hub by 2027, covering AI infrastructure, talent, innovation, and industry adoption"
                },
                {
                    "name": "AI Ethics Guidelines",
                    "url": "https://www.nstda.or.th/th/nstda-knowledge/16621-ai-ethics",
                    "desc": "NSTDA framework for ethical AI development ensuring transparency, accountability, fairness, and human-centric AI systems in Thailand"
                },
                {
                    "name": "Thailand 4.0",
                    "url": "https://www.boi.go.th/index.php?page=demographic",
                    "desc": "National economic model integrating AI across target industries (next-gen automotive, smart electronics, medical hub, robotics, aviation, biofuels) to drive innovation-led growth"
                },
                {
                    "name": "AI for Good for All (AІГА)",
                    "url": "https://www.depa.or.th/en/ai-initiative",
                    "desc": "DEPA initiative promoting responsible AI adoption, digital skills training, and AI solutions for social good across Thai communities"
                },
                {
                    "name": "National Science and Technology Development Agency (NSTDA)",
                    "url": "https://www.nstda.or.th/home/",
                    "desc": "Leading Thailand's AI research, innovation, and talent development with focus on manufacturing, agriculture, healthcare, and tourism applications"
                }
            ]
        },
        {
            "subtitle": "Malaysia",
            "items": [
                {
                    "name": "National AI Roadmap (AI-RMAP 2021-2025)",
                    "url": "https://www.malaysia.gov.my/portal/content/31794",
                    "desc": "Comprehensive 5-year strategy with 6 strategic thrusts: AI governance, talent, adoption, data ecosystem, compute infrastructure, and innovation for public services, manufacturing, agriculture, and healthcare"
                },
                {
                    "name": "AI Governance Framework",
                    "url": "https://www.mdec.my/digital-economy-initiatives/national-ai-framework",
                    "desc": "Ethical guidelines and governance principles for responsible AI deployment in Malaysia, emphasizing transparency, accountability, and human rights"
                },
                {
                    "name": "MyDIGITAL Initiative",
                    "url": "https://www.malaysia.gov.my/portal/content/31798",
                    "desc": "National digital economy blueprint (2021-2030) positioning AI as key enabler for economic transformation, targeting 22.6% GDP contribution from digital economy"
                },
                {
                    "name": "Malaysia Digital Economy Corporation (MDEC)",
                    "url": "https://mdec.my/",
                    "desc": "Government agency driving AI adoption, digital transformation, and tech talent development through programmes, funding, and industry partnerships"
                },
                {
                    "name": "National AI Office (NAIO)",
                    "url": "https://www.malaysia.gov.my/portal/content/31794",
                    "desc": "Coordinating body under MOSTI overseeing AI-RMAP implementation, policy development, and cross-agency collaboration on national AI initiatives"
                }
            ]
        }
    ]
}

print("Fetching current winners_payload for year 2026...")
response = supabase.table("winners_payload").select("payload").eq("year", 2026).execute()

if not response.data:
    print("ERROR: No data found for year 2026")
    exit(1)

payload = response.data[0]["payload"]
sections = payload.get("sections", [])

# Replace the first section with the new regional structure
sections[0] = regional_section

print("Updated section structure:")
print(f"  Title: {regional_section['title']}")
print(f"  Countries: {len(regional_section['categories'])}")
for cat in regional_section['categories']:
    country = cat['subtitle']
    count = len(cat['items'])
    print(f"    - {country}: {count} items")

total_items = sum(len(cat['items']) for cat in regional_section['categories'])
print(f"\n  Total items: {total_items}")

# Update database
print("\nUpdating database...")
update_response = supabase.table("winners_payload").update({"payload": {"sections": sections}}).eq("year", 2026).execute()

print("✓ Successfully updated to regional ASEAN AI framework")
print("✓ Section now covers Singapore, Indonesia, Thailand, and Malaysia")
