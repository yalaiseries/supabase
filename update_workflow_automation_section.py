"""
Update Section 2: Workflow Automation & AI Agents (2025 Trends)
Focus: Agent runtimes, visual builders, automation platforms, generative media, AI coding assistants
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

# Section 2 data: Workflow Automation & AI Agents (2025 Trends)
workflow_categories = [
    {
        "subtitle": "Agent runtimes (brains / reasoning layer)",
        "items": [
            {
                "name": "LangChain / LangGraph / LangSmith",
                "url": "https://www.langchain.com/",
                "desc": "Core Python/RAG + graph‑based agent runtime + tracing/observability."
            },
            {
                "name": "CrewAI",
                "url": "https://github.com/crewAIInc/crewAI",
                "desc": "Multi‑agent 'crew / role / task' framework in Python."
            },
            {
                "name": "AutoGen",
                "url": "https://github.com/microsoft/autogen",
                "desc": "Multi‑agent LLM‑LLM/LLM‑human collaboration framework."
            },
            {
                "name": "Agno",
                "url": "https://github.com/agno-agi/agno",
                "desc": "Typed, production‑oriented agent framework for Python."
            },
            {
                "name": "Pydantic‑AI",
                "url": "https://github.com/pydantic/pydantic-ai",
                "desc": "Schema‑first agent layer with strict Pydantic validation."
            }
        ]
    },
    {
        "subtitle": "Visual LLM / agent builders (canvas & low‑code)",
        "items": [
            {
                "name": "Langflow",
                "url": "https://www.langflow.org/",
                "desc": "Visual builder for chains, agents, RAG, on top of LangChain‑style components."
            },
            {
                "name": "Flowise AI",
                "url": "https://flowiseai.com/",
                "desc": "OSS visual builder for LLM chatbots and RAG flows."
            },
            {
                "name": "SmythOS",
                "url": "https://smythos.com/",
                "desc": "No‑code orchestrator for fleets of AI agents and tools."
            },
            {
                "name": "GPTBots.ai",
                "url": "https://gptbots.ai/",
                "desc": "Enterprise platform for building and deploying AI agents."
            },
            {
                "name": "Respell",
                "url": "https://www.respell.ai/",
                "desc": "Natural‑language and node‑based 'spell' builder for AI workflows."
            }
        ]
    },
    {
        "subtitle": "Automation & integration (orchestration / plumbing)",
        "items": [
            {
                "name": "n8n",
                "url": "https://n8n.io/",
                "desc": "OSS visual workflow automation (APIs, DBs, AI nodes, JS/Python)."
            },
            {
                "name": "Make",
                "url": "https://www.make.com/",
                "desc": "Cloud scenarios + AI modules for SaaS automation."
            },
            {
                "name": "Zapier",
                "url": "https://zapier.com/",
                "desc": "Mass‑market automation with AI Actions and agents."
            },
            {
                "name": "Workato",
                "url": "https://www.workato.com/",
                "desc": "Enterprise iPaaS with AI 'recipes' and governance."
            },
            {
                "name": "Tray.io",
                "url": "https://tray.io/",
                "desc": "Low‑code iPaaS for complex API workflows with AI connectors."
            },
            {
                "name": "Power Automate",
                "url": "https://powerautomate.microsoft.com/",
                "desc": "M365‑centric automation with Copilot‑assisted flow building."
            },
            {
                "name": "Whalesync",
                "url": "https://www.whalesync.com/",
                "desc": "Real‑time 2‑way data sync between SaaS apps and databases."
            }
        ]
    },
    {
        "subtitle": "Generative media & creative workflows",
        "items": [
            {
                "name": "ComfyUI",
                "url": "https://github.com/comfyanonymous/ComfyUI",
                "desc": "Node‑based engine for image/video/3D/audio generation workflows."
            },
            {
                "name": "Trellis",
                "url": "https://github.com/microsoft/TRELLIS",
                "desc": "Image‑to‑3D workflow/model stack on this style of pipeline."
            },
            {
                "name": "Vid2Vid Dance",
                "url": "https://openart.ai/workflows/bananasss/vid2vid-dance/KpkvqxEsgJbqN5M1jJJg",
                "desc": "Motion/dance transfer video→video workflow."
            },
            {
                "name": "Flux Fill",
                "url": "https://github.com/comfyanonymous/ComfyUI_examples",
                "desc": "Inpainting/outpainting ComfyUI example workflows."
            },
            {
                "name": "AnimateDiff Evolved",
                "url": "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved",
                "desc": "Video stylization and reanimation pipeline."
            },
            {
                "name": "Fluxtapoz",
                "url": "https://civitai.com/models/618069",
                "desc": "RF inversion & strong stylization workflow/model."
            },
            {
                "name": "CogVideoX",
                "url": "https://github.com/THUDM/CogVideo",
                "desc": "Open text/image‑to‑video diffusion model family."
            },
            {
                "name": "Hallo2",
                "url": "https://github.com/fudan-generative-vision/hallo2",
                "desc": "Audio‑driven lip‑sync talking‑head pipeline."
            }
        ]
    },
    {
        "subtitle": "AI‑first no‑code app builders (AI coders)",
        "items": [
            {
                "name": "Base44",
                "url": "https://base44.com/",
                "desc": "AI no‑code platform that turns NL app specs into full web apps with backend, auth, and hosting."
            }
        ]
    },
    {
        "subtitle": "Conversational AI shells (chat layer)",
        "items": [
            {
                "name": "Rasa",
                "url": "https://rasa.com/",
                "desc": "OSS NLU + dialogue manager for intent‑driven assistants that can call tools."
            },
            {
                "name": "Botpress",
                "url": "https://botpress.com/",
                "desc": "Visual conversational AI platform for LLM‑enhanced chatbots across channels."
            }
        ]
    },
    {
        "subtitle": "AI coding assistants (developer tooling)",
        "items": [
            {
                "name": "GitHub Copilot (VS Code)",
                "url": "https://code.visualstudio.com/docs/copilot/overview",
                "desc": "AI pair‑programmer embedded in VS Code that suggests code, explains/debugs, and now supports agent‑like 'Plan Mode' and sub‑agents for multi‑step coding tasks."
            },
            {
                "name": "OpenAI Codex / GPT‑5‑Codex (ChatGPT code agent)",
                "url": "https://github.com/features/copilot",
                "desc": "OpenAI's coding agent (now using GPT‑5‑Codex) that can take on longer coding tasks end‑to‑end, available in IDEs, terminal, and ChatGPT as a more autonomous code worker."
            }
        ]
    }
]

def update_workflow_section():
    """Update Section 2: Workflow Automation & AI Agents"""
    
    print("Fetching current data from Supabase...")
    
    # Fetch the current 2026 winners data
    response = supabase.table("winners_payload").select("*").eq("year", 2026).execute()
    
    if not response.data or len(response.data) == 0:
        print("❌ No 2026 data found")
        return
    
    record = response.data[0]
    payload = record['payload']
    
    # Find or create Section 2
    section_index = None
    for i, section in enumerate(payload['sections']):
        if '2.' in section['title'] or 'Workflow Automation' in section['title']:
            section_index = i
            break
    
    if section_index is not None:
        # Update existing Section 2
        payload['sections'][section_index]['title'] = '2. Workflow Automation & AI Agents (2025 Trends)'
        payload['sections'][section_index]['categories'] = workflow_categories
        print(f"✅ Updated Section 2: {payload['sections'][section_index]['title']}")
    else:
        # Create new Section 2
        new_section = {
            'title': '2. Workflow Automation & AI Agents (2025 Trends)',
            'categories': workflow_categories
        }
        # Insert after Section 1
        if len(payload['sections']) > 1:
            payload['sections'].insert(1, new_section)
        else:
            payload['sections'].append(new_section)
        print("✅ Created new Section 2: Workflow Automation & AI Agents (2025 Trends)")
    
    # Count total items
    total_items = sum(len(cat['items']) for cat in workflow_categories)
    print(f"\nTotal categories: {len(workflow_categories)}")
    print(f"Total tools/platforms: {total_items}")
    
    # Update the database
    print("\nUpdating database...")
    update_response = supabase.table("winners_payload").update({
        "payload": payload
    }).eq("year", 2026).execute()
    
    if update_response.data:
        print("✅ Database updated successfully!")
        print(f"\nCategories added:")
        for i, category in enumerate(workflow_categories, 1):
            print(f"{i}. {category['subtitle']} ({len(category['items'])} items)")
    else:
        print("❌ Database update failed")

if __name__ == "__main__":
    update_workflow_section()
