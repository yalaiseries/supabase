#!/usr/bin/env python3
"""
Verify all sections in winners_payload year=2026
"""
import os
import json
from supabase import create_client, Client

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("Fetching winners_payload year=2026 sections...")
try:
    result = supabase.table('winners_payload').select('payload').eq('year', 2026).execute()
    
    if not result.data:
        print("❌ No year=2026 found!")
        exit(1)
    
    payload = result.data[0].get('payload', {})
    sections = payload.get('sections', [])
    
    print(f"\n✅ Total sections: {len(sections)}\n")
    print("="*80)
    
    for section in sections:
        title = section.get('title', 'No title')
        categories = section.get('categories', [])
        total_items = sum(len(cat.get('items', [])) for cat in categories)
        
        print(f"\n{title}")
        print(f"  Categories: {len(categories)}, Total items: {total_items}")
        
        for cat in categories:
            subtitle = cat.get('subtitle', 'No subtitle')
            items = cat.get('items', [])
            print(f"    - {subtitle}: {len(items)} items")
    
    print("\n" + "="*80)
    print(f"\n✅ All {len(sections)} sections are present!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
