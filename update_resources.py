#!/usr/bin/env python3
"""
Update AI/AECO resources in Supabase from resources-complete.json
Table schema: title, url, note, sort_order, active
"""
import json
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

# Load resources data
with open('data/resources-complete.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

year = data['year']
sections = data['payload']['sections']

print(f"Loading resources for year {year}...")
print(f"Found {len(sections)} sections")

# Flatten the structure into individual resource items
# Schema: title, url, note, sort_order, active
resources = []
sort_order = 1

for section in sections:
    section_title = section['title']
    for category in section.get('categories', []):
        category_subtitle = category.get('subtitle', '')
        for item in category.get('items', []):
            # Combine section, category, and name into title
            title = f"{section_title.split('.')[1].strip()} - {category_subtitle} - {item['name']}"
            
            # Combine description and video into note
            note_parts = []
            if item.get('desc'):
                note_parts.append(item['desc'])
            if item.get('video'):
                note_parts.append(f"Video: {item['video']}")
            note = ' | '.join(note_parts) if note_parts else None
            
            resource = {
                'title': title,
                'url': item['url'],
                'note': note,
                'sort_order': sort_order,
                'active': True
            }
            resources.append(resource)
            sort_order += 1

print(f"Prepared {len(resources)} resources for upload")

# Delete all existing resources (table doesn't have year column)
print(f"Deleting all existing resources...")
try:
    result = supabase.table('members_resources').delete().neq('id', 0).execute()
    print(f"Deleted existing records")
except Exception as e:
    print(f"Delete error (may be okay if no existing data): {e}")

# Insert new resources in batches
batch_size = 100
for i in range(0, len(resources), batch_size):
    batch = resources[i:i+batch_size]
    try:
        result = supabase.table('members_resources').insert(batch).execute()
        print(f"Inserted batch {i//batch_size + 1} ({len(batch)} items)")
    except Exception as e:
        print(f"ERROR inserting batch {i//batch_size + 1}: {e}")
        print(f"First item in failed batch: {batch[0]}")
        exit(1)


print(f"\n✅ Successfully uploaded {len(resources)} resources to Supabase!")
print(f"Table: members_resources")
print(f"Resources organized by section/category with sort order")

