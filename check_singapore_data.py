#!/usr/bin/env python3
import os
import json
from supabase import create_client

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Fetch the winners_payload for year 2026
response = supabase.table("winners_payload").select("payload").eq("year", 2026).execute()

if response.data:
    payload = response.data[0]["payload"]
    sections = payload.get("sections", [])
    
    print(f"Total sections: {len(sections)}\n")
    
    for i, section in enumerate(sections, 1):
        print(f"Section {i}: {section.get('title', 'NO TITLE')}")
        if section.get('title') == "1. AI Framework & Strategy (Singapore)":
            print("  FOUND SINGAPORE SECTION!")
            for j, category in enumerate(section.get('categories', []), 1):
                print(f"  Category {j}: {category.get('subtitle', 'NO SUBTITLE')}")
                items = category.get('items', [])
                print(f"    Items count: {len(items)}")
                for k, item in enumerate(items, 1):
                    name = item.get('name', 'NO NAME')
                    desc = item.get('desc', '')
                    url = item.get('url', 'NO URL')
                    print(f"    {k}. {name}")
                    print(f"       desc: '{desc}'")
                    print(f"       url: {url}")
else:
    print("No data found for year 2026")
