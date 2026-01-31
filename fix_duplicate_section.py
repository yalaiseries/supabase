#!/usr/bin/env python3
"""
Fix duplicate AI Framework & Strategy sections by merging them
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
    
    print(f"Current state: {len(sections)} sections")
    
    # Remove section 2 (the old duplicate) and keep only section 1 (the complete one with 7 items)
    # Section 1 already has all 7 resources properly organized
    new_sections = [sections[0]]  # Keep the first one (my new complete section)
    new_sections.extend(sections[2:])  # Add sections 3-8 (skip section 2 - the old one)
    
    # Renumber sections
    for i, section in enumerate(new_sections, start=1):
        if 'title' in section:
            title = section['title']
            # Remove old number prefix
            if '. ' in title:
                title = title.split('. ', 1)[1]
            section['title'] = f"{i}. {title}"
    
    payload['sections'] = new_sections
    
    print(f"\nRemoving duplicate section...")
    print(f"New section count: {len(new_sections)}")
    
    # Update database
    update_result = supabase.table('winners_payload').update({
        'payload': payload
    }).eq('year', 2026).execute()
    
    print(f"\n✅ Fixed! Now have {len(new_sections)} sections:")
    for i, section in enumerate(new_sections, 1):
        title = section.get('title', 'Unknown')
        categories = section.get('categories', [])
        total_items = sum(len(cat.get('items', [])) for cat in categories)
        print(f"  {title} ({total_items} items)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n✅ Done! Duplicate removed and sections renumbered correctly.")
