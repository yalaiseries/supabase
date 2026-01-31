"""
Update Section 3: Generative Imaging & Design Visualization Tools
Focus: Core model hubs, image generation platforms, AEC/architecture tools, video/multimodal, local UIs
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

# Section 3 data: Generative Imaging & Design Visualization Tools
imaging_categories = [
    {
        "subtitle": "Core model hubs & ecosystems",
        "items": [
            {
                "name": "Hugging Face",
                "url": "https://huggingface.co/",
                "desc": "Central hub for open‑source models (SD, SDXL, ControlNet, LoRA) and ready‑to-run Spaces for generative workflows."
            },
            {
                "name": "Stable Diffusion (code)",
                "url": "https://github.com/Stability-AI/stablediffusion",
                "desc": "Open‑source latent diffusion model family that powers many third‑party generators."
            },
            {
                "name": "Stability AI (SDXL)",
                "url": "https://stability.ai/stable-diffusion",
                "desc": "Official SDXL models with higher quality, resolution, and style control than earlier SD releases."
            }
        ]
    },
    {
        "subtitle": "General image generation platforms",
        "items": [
            {
                "name": "Dezgo",
                "url": "https://dezgo.com/",
                "desc": "Browser‑based Stable Diffusion service with text‑to‑image, image‑to‑image, and ControlNet support for quick experiments."
            },
            {
                "name": "Getimg.ai",
                "url": "https://getimg.ai/",
                "desc": "Web suite for text‑to‑image, editor, inpainting, and custom model workflows with a simple UI."
            },
            {
                "name": "KREA",
                "url": "https://www.krea.ai/",
                "desc": "Real‑time generative suite where sketches and masks update into final images or videos instantly, ideal for live ideation."
            },
            {
                "name": "Lexica",
                "url": "https://lexica.art/",
                "desc": "Searchable gallery and generator for Stable Diffusion images and prompts, useful for studying styles and prompt patterns."
            },
            {
                "name": "OpenArt",
                "url": "https://openart.ai/",
                "desc": "Community image platform that hosts models, prompts, and ComfyUI workflows alongside a web generator."
            },
            {
                "name": "Midjourney",
                "url": "https://www.midjourney.com/",
                "desc": "High‑quality, style‑strong image generator operated via Discord, popular for concept art and visual moodboards."
            },
            {
                "name": "DALL‑E 3",
                "url": "https://openai.com/dall-e-3",
                "desc": "OpenAI's text‑to‑image model with strong prompt understanding and integration into ChatGPT and other products."
            },
            {
                "name": "Stable Diffusion Web",
                "url": "https://stablediffusionweb.com/",
                "desc": "Hosted Web UI for Stable Diffusion providing advanced options directly in the browser."
            },
            {
                "name": "Unstability / Unstable Diffusion",
                "url": "https://www.unstability.ai/",
                "desc": "Uncensored image‑generation platform offering multiple community models behind a credit system."
            },
            {
                "name": "Prodia",
                "url": "https://prodia.com/",
                "desc": "Ultra‑fast, API‑centric image generation service optimized for low‑latency, high‑volume use cases."
            },
            {
                "name": "Freepik Pikaso",
                "url": "https://www.freepik.com/pikaso",
                "desc": "Drawing‑oriented AI tools (sketch to render, simple edits) integrated into the Freepik ecosystem."
            },
            {
                "name": "PixAI",
                "url": "https://pixai.art/",
                "desc": "Anime‑focused generator and community, with tools for stylized characters and figures."
            }
        ]
    },
    {
        "subtitle": "AEC / architecture‑specific tools",
        "items": [
            {
                "name": "ArkoAI",
                "url": "https://www.arko.ai/",
                "desc": "Revit‑integrated AI rendering tool to generate concept images directly from BIM views."
            },
            {
                "name": "LookX",
                "url": "https://www.lookx.ai/",
                "desc": "Architecture‑oriented AI platform for massing, facades, and early‑stage design imagery."
            },
            {
                "name": "Veras",
                "url": "https://www.veras.ai/",
                "desc": "Plugin that renders AI overlays from Revit/Rhino views, preserving underlying geometry while exploring styles."
            },
            {
                "name": "Visoid",
                "url": "https://visoid.com/",
                "desc": "AI visualization platform aimed at architects and urban designers for site and massing concepts."
            },
            {
                "name": "roomGPT",
                "url": "https://www.roomgpt.io/",
                "desc": "Photo‑based interior design tool that generates styled redesigns of existing rooms."
            }
        ]
    },
    {
        "subtitle": "Video & multimodal",
        "items": [
            {
                "name": "Runway",
                "url": "https://runwayml.com/",
                "desc": "Web platform for text‑to‑video, image‑to‑video, green‑screen, and editing workflows aimed at creators and editors."
            },
            {
                "name": "Pika",
                "url": "https://pika.art/",
                "desc": "Text‑to‑video and image‑to‑video generator with strong stylization for short clips and animations."
            },
            {
                "name": "KREA Realtime Video",
                "url": "https://github.com/krea-ai/realtime-video",
                "desc": "Open‑source, real‑time video model (Krea Realtime 14B) for sketch‑to‑video usage."
            }
        ]
    },
    {
        "subtitle": "Local UIs, control & tutorials",
        "items": [
            {
                "name": "AUTOMATIC1111 WebUI",
                "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
                "desc": "Popular local Stable Diffusion interface with plug‑ins for ControlNet, LoRA, and upscalers."
            },
            {
                "name": "ControlNet Models",
                "url": "https://huggingface.co/lllyasviel/ControlNet/tree/main/models",
                "desc": "Library of ControlNet checkpoints (canny, depth, pose, etc.) to add structure/control to SD outputs."
            },
            {
                "name": "ComfyUI Tutorial",
                "url": "https://www.youtube.com/watch?v=Zko_s2LO9Wo",
                "desc": "Intro video for installing and building node‑based SD workflows in ComfyUI."
            },
            {
                "name": "Google Colab (LoRA)",
                "url": "https://colab.research.google.com/",
                "desc": "Cloud notebook platform widely used to train LoRA adapters and run SD/SDXL notebooks without a local GPU."
            }
        ]
    }
]

def update_imaging_section():
    """Update Section 3: Generative Imaging & Design Visualization Tools"""
    
    print("Fetching current data from Supabase...")
    
    # Fetch the current 2026 winners data
    response = supabase.table("winners_payload").select("*").eq("year", 2026).execute()
    
    if not response.data or len(response.data) == 0:
        print("❌ No 2026 data found")
        return
    
    record = response.data[0]
    payload = record['payload']
    
    # Find or create Section 3
    section_index = None
    for i, section in enumerate(payload['sections']):
        if '3.' in section['title'] or 'Generative AI' in section['title'] or 'Visualisation' in section['title']:
            section_index = i
            break
    
    if section_index is not None:
        # Update existing Section 3
        payload['sections'][section_index]['title'] = '3. Generative Imaging & Design Visualization Tools'
        payload['sections'][section_index]['categories'] = imaging_categories
        print(f"✅ Updated Section 3: {payload['sections'][section_index]['title']}")
    else:
        # Create new Section 3
        new_section = {
            'title': '3. Generative Imaging & Design Visualization Tools',
            'categories': imaging_categories
        }
        # Insert after Section 2
        if len(payload['sections']) > 2:
            payload['sections'].insert(2, new_section)
        else:
            payload['sections'].append(new_section)
        print("✅ Created new Section 3: Generative Imaging & Design Visualization Tools")
    
    # Count total items
    total_items = sum(len(cat['items']) for cat in imaging_categories)
    print(f"\nTotal categories: {len(imaging_categories)}")
    print(f"Total tools/platforms: {total_items}")
    
    # Update the database
    print("\nUpdating database...")
    update_response = supabase.table("winners_payload").update({
        "payload": payload
    }).eq("year", 2026).execute()
    
    if update_response.data:
        print("✅ Database updated successfully!")
        print(f"\nCategories added:")
        for i, category in enumerate(imaging_categories, 1):
            print(f"{i}. {category['subtitle']} ({len(category['items'])} items)")
    else:
        print("❌ Database update failed")

if __name__ == "__main__":
    update_imaging_section()
