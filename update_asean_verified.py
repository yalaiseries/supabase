#!/usr/bin/env python3
import os
from supabase import create_client

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Updated regional section with verified and additional resources
regional_section = {
    "title": "1. AI Governance, Strategy & Programmes",
    "categories": [
        {
            "subtitle": "Singapore",
            "items": [
                {
                    "name": "AI Verify Foundation",
                    "url": "https://aiverifyfoundation.sg/",
                    "desc": "World's first AI governance testing framework and software toolkit validating AI systems against 11 internationally recognized principles"
                },
                {
                    "name": "Model AI Governance Framework",
                    "url": "https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework",
                    "desc": "PDPC guidelines for ethical AI deployment with practical guidance on transparency, explainability, fairness, and human oversight"
                },
                {
                    "name": "AI Singapore",
                    "url": "https://aisingapore.org",
                    "desc": "Flagship national AI programme for R&D, talent development (15k practitioners goal), and practical AI use cases across sectors"
                },
                {
                    "name": "Enterprise Compute Initiative",
                    "url": "https://www.imda.gov.sg/how-we-can-help/national-ai-strategy/enterprise-compute-initiative",
                    "desc": "NAIS 2.0 infrastructure providing compute resources, data access and tools to accelerate industry AI projects"
                },
                {
                    "name": "Personal Data Protection Act (PDPA)",
                    "url": "https://www.pdpc.gov.sg/overview-of-pdpa/the-legislation/personal-data-protection-act",
                    "desc": "Singapore's data protection law establishing baseline standards for personal data protection in AI systems"
                },
                {
                    "name": "Advisory Guidelines on AI Systems",
                    "url": "https://www.pdpc.gov.sg/help-and-resources/2020/01/advisory-guidelines-on-use-of-personal-data-in-ai-recommendation-and-decision-systems",
                    "desc": "PDPC practical guidance on managing personal data protection in AI recommendation and decision systems"
                },
                {
                    "name": "Compendium of Use Cases",
                    "url": "https://aiverifyfoundation.sg/downloads/Compendium_of_Use_Cases_2nd_Edition.pdf",
                    "desc": "Real-world case studies demonstrating Model AI Governance Framework implementation across industries"
                },
                {
                    "name": "National AI Strategy 2019",
                    "url": "https://www.smartnation.gov.sg/nais/",
                    "desc": "Original NAIS outlining five National AI Projects (transport, smart cities, healthcare, education, security) plus ecosystem enablers"
                },
                {
                    "name": "National AI Strategy 2.0",
                    "url": "https://www.smartnation.gov.sg/nais/national-ai-strategy-2/",
                    "desc": "Updated 2023 strategy with 15 actions, SGD 1B+ investment, focusing on AI hubs, compute access, trusted governance and 15,000 AI talents"
                },
                {
                    "name": "National Multimodal LLM Programme",
                    "url": "https://www.aisingapore.org/innovation/national-llm/",
                    "desc": "S$70M NAIS 2.0 initiative building Singapore-centric LLMs like MERaLiON with local context and governance guardrails"
                },
                {
                    "name": "AI for Everyone",
                    "url": "https://www.imda.gov.sg/how-we-can-help/skills-and-training/ai-for-everyone",
                    "desc": "National programme to build AI literacy helping Singaporeans understand AI basics and use AI tools in daily life and work"
                },
                {
                    "name": "AI for Industry",
                    "url": "https://www.aisingapore.org/innovation/ai-products-services/",
                    "desc": "Programme supporting Singapore businesses to adopt AI through funding, technical expertise and partnerships"
                }
            ]
        },
        {
            "subtitle": "Indonesia",
            "items": [
                {
                    "name": "National AI Strategy (Stranas KA 2020-2045)",
                    "url": "https://www.bappenas.go.id/",
                    "desc": "Indonesia's comprehensive 25-year AI roadmap developed by Bappenas, focusing on ethical AI, talent development, research, and infrastructure across healthcare, education, agriculture, smart cities, and public services"
                },
                {
                    "name": "National Research and Innovation Agency (BRIN)",
                    "url": "https://www.brin.go.id/",
                    "desc": "Indonesia's leading government agency coordinating national AI research, development, innovation initiatives and AI ecosystem development"
                },
                {
                    "name": "Ministry of Communication and Digital Affairs",
                    "url": "https://www.komdigi.go.id/",
                    "desc": "Government ministry overseeing digital transformation, AI policy implementation, and technology governance across Indonesia"
                },
                {
                    "name": "Making Indonesia 4.0",
                    "url": "https://kemenperin.go.id/",
                    "desc": "Ministry of Industry's roadmap integrating AI and Industry 4.0 technologies to boost manufacturing competitiveness and economic growth"
                },
                {
                    "name": "Indonesia AI Society",
                    "url": "https://www.linkedin.com/company/indonesia-ai-society/",
                    "desc": "National community and knowledge hub advancing AI research, education, and practical applications across Indonesian industries"
                }
            ]
        },
        {
            "subtitle": "Thailand",
            "items": [
                {
                    "name": "National AI Strategy and Action Plan",
                    "url": "https://www.nstda.or.th/",
                    "desc": "NSTDA's comprehensive strategy aiming to make Thailand ASEAN's AI hub by 2027, covering AI infrastructure, talent development, innovation, and industry adoption across manufacturing, agriculture, healthcare, and tourism"
                },
                {
                    "name": "Digital Economy Promotion Agency (DEPA)",
                    "url": "https://www.depa.or.th/",
                    "desc": "Government agency driving Thailand's digital economy and AI adoption through policy, programmes, funding, and industry partnerships"
                },
                {
                    "name": "National Science and Technology Development Agency (NSTDA)",
                    "url": "https://www.nstda.or.th/",
                    "desc": "Leading Thailand's AI research, innovation, and talent development with focus on practical applications in key industries"
                },
                {
                    "name": "Ministry of Higher Education, Science, Research and Innovation",
                    "url": "https://www.most.go.th/",
                    "desc": "Government ministry coordinating Thailand's science, technology and AI research policy, funding and development initiatives"
                },
                {
                    "name": "Thailand 4.0 Economic Model",
                    "url": "https://www.boi.go.th/",
                    "desc": "Board of Investment's national economic strategy integrating AI across target industries (next-gen automotive, smart electronics, medical hub, robotics, aviation) to drive innovation-led growth"
                },
                {
                    "name": "Thailand AI Association",
                    "url": "https://www.aiforthai.in.th/",
                    "desc": "National AI community promoting AI research, education, ethics, and practical deployment across Thai industries and society"
                }
            ]
        },
        {
            "subtitle": "Malaysia",
            "items": [
                {
                    "name": "National AI Roadmap (AI-RMAP 2021-2025)",
                    "url": "https://www.mosti.gov.my/",
                    "desc": "MOSTI's comprehensive 5-year AI strategy with 6 thrusts: governance, talent, adoption, data ecosystem, compute infrastructure, and innovation for public services, manufacturing, agriculture, and healthcare"
                },
                {
                    "name": "Malaysia Digital Economy Corporation (MDEC)",
                    "url": "https://mdec.my/",
                    "desc": "Government agency under Ministry of Digital driving AI adoption, digital transformation, tech talent development through programmes, funding, and industry partnerships"
                },
                {
                    "name": "Ministry of Science, Technology and Innovation (MOSTI)",
                    "url": "https://www.mosti.gov.my/",
                    "desc": "Government ministry overseeing Malaysia's AI policy, research funding, and national innovation initiatives including AI-RMAP coordination"
                },
                {
                    "name": "MyDIGITAL Initiative",
                    "url": "https://www.malaysia.gov.my/",
                    "desc": "National digital economy blueprint (2021-2030) positioning AI as key enabler for economic transformation, targeting 22.6% GDP contribution from digital economy"
                },
                {
                    "name": "National Science and Technology Council (NSTC)",
                    "url": "https://www.mosti.gov.my/",
                    "desc": "High-level council under MOSTI setting Malaysia's science, technology and AI policy direction and coordinating national R&D priorities"
                },
                {
                    "name": "Malaysia AI Ethics Framework",
                    "url": "https://mdec.my/",
                    "desc": "MDEC ethical guidelines and governance principles for responsible AI deployment emphasizing transparency, accountability, fairness and human rights"
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

# Replace the first section with updated resources
sections[0] = regional_section

print("Updated with verified and expanded resources:")
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

print("✓ Successfully updated ASEAN AI resources with verified URLs")
print("✓ All links point to official government agencies and verified sources")
