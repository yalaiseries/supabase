#!/usr/bin/env python3
"""
Check current state of winners_payload year=2026 and fix duplicate section
"""
import os
import json
from supabase import create_client, Client

# Load Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("Fetching current winners_payload for year=2026...")
try:
    result = supabase.table('winners_payload').select('*').eq('year', 2026).execute()
    
    if not result.data:
        print("❌ No year=2026 entry found!")
        exit(1)
    
    current_row = result.data[0]
    payload = current_row.get('payload', {})
    sections = payload.get('sections', [])
    
    print(f"\n✅ Found {len(sections)} sections:\n")
    for i, section in enumerate(sections, 1):
        title = section.get('title', 'Unknown')
        categories = section.get('categories', [])
        total_items = sum(len(cat.get('items', [])) for cat in categories)
        print(f"{i}. {title}")
        print(f"   Categories: {len(categories)}, Total items: {total_items}")
        for cat in categories:
            print(f"   - {cat.get('subtitle', 'No subtitle')}: {len(cat.get('items', []))} items")
        print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
