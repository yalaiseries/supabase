import json

# Extract the resources data structure
resources_data = {
  "sections": [
    {
      "title": "1. AI Framework & Strategy (Singapore)",
      "categories": [
        {
          "subtitle": "Governance & Policy",
          "items": [
            {"name": "Artificial Intelligence Singapore", "url": "https://www.aisingapore.org", "desc": "Strategic overview of Singapore's national AI tech pillars."},
            {"name": "AI Governance Testing Framework", "url": "https://aiverifyfoundation.sg", "desc": "\"AI Verify\" toolkit for self-assessing AI systems against ethical principles."},
            {"name": "AI Governance Framework", "url": "https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework", "desc": "Official guidelines for implementing ethical and transparent AI in organizations."},
            {"name": "Compendium of Use Cases", "url": "https://file.go.gov.sg/aiverify-usecase.pdf", "desc": "PDF collection of real-world AI applications across various sectors."},
            {"name": "IMDA GenAI Consultation", "url": "https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2023/imda-launches-public-consultation-on-proposed-governance-approach-for-generative-ai", "desc": "News on the Model AI Governing Framework specifically for Generative AI."}
          ]
        }
      ]
    },
    {
      "title": "2. Workflow Automation & AI Agents (2025 Trends)",
      "categories": [
        {
          "subtitle": "Agent Builders & Orchestration",
          "items": [
            {"name": "n8n", "url": "https://n8n.io", "desc": "Open-source visual workflow automation tool with over 200 integrations."},
            {"name": "Langflow", "url": "https://www.langflow.org", "desc": "Visual programming for LLM chains and agents, supporting the Model Context Protocol."},
            {"name": "ComfyUI", "url": "https://github.com/comfyanonymous/ComfyUI", "desc": "Modular node-based interface for advanced generative AI workflows.", "video": "https://www.youtube.com/results?search_query=comfyui+tutorial"},
            {"name": "Flowise", "url": "https://flowiseai.com", "desc": "Visual builder for chaining LLMs, similar to Langflow."},
            {"name": "SmythOS", "url": "https://smythos.com", "desc": "Drag-and-drop AI agent builder with multi-model orchestration."},
            {"name": "GPTBots.ai", "url": "https://gptbots.ai", "desc": "Enterprise platform for AI agent building and automation."},
            {"name": "Respell", "url": "https://www.respell.ai", "desc": "No-code platform for creating AI agents using natural language."},
            {"name": "Make", "url": "https://www.make.com", "desc": "Cloud-based automation platform with AI modules (formerly Integromat)."},
            {"name": "Zapier", "url": "https://zapier.com", "desc": "Automation tool featuring AI and LLM actions."},
            {"name": "Workato", "url": "https://www.workato.com", "desc": "Enterprise integration and automation platform."},
            {"name": "Tray.io", "url": "https://tray.io", "desc": "Low-code automation platform with AI connectors."},
            {"name": "Power Automate", "url": "https://powerautomate.microsoft.com", "desc": "Microsoft's automation solution integrated with Copilot."},
            {"name": "Whalesync", "url": "https://www.whalesync.com", "desc": "Tool for syncing data between SaaS apps with AI capabilities."}
          ]
        },
        {
          "subtitle": "ComfyUI Community Workflows",
          "items": [
            {"name": "Trellis", "url": "https://github.com/microsoft/TRELLIS", "desc": "Workflow for converting images to 3D models."},
            {"name": "Vid2Vid Dance", "url": "https://openart.ai/workflows/bananasss/vid2vid-dance/KpkvqxEsgJbqN5M1jJJg", "desc": "Transferring motion/dance from video to video."},
            {"name": "Flux Fill", "url": "https://github.com/comfyanonymous/ComfyUI_examples", "desc": "Workflow for image inpainting and outpainting."},
            {"name": "AnimateDiff", "url": "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved", "desc": "Video-to-video workflow using ControlNet and auto-masking."},
            {"name": "Fluxtapoz", "url": "https://civitai.com/models/618069", "desc": "RF inversion and stylization workflow."},
            {"name": "CogVideoX", "url": "https://github.com/THUDM/CogVideo", "desc": "Image-to-video generation model."},
            {"name": "Hallo2", "url": "https://github.com/fudan-generative-vision/hallo2", "desc": "Lip-syncing portrait workflow driven by audio."}
          ]
        }
      ]
    }
  ]
}

# Save to JSON file
with open('data/resources-data.json', 'w', encoding='utf-8') as f:
    json.dump(resources_data, f, indent=2, ensure_ascii=False)

print("Created data/resources-data.json")
print("Note: This is a starting template - you'll need to add all the other sections from resources.html")
