import os
from supabase import create_client, Client

# Initialize Supabase client
url = "https://gxffygzbyzpocptgzfdc.supabase.co"
key = os.environ.get('SUPABASE_SERVICE_KEY')

if not key:
    print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
    exit(1)

supabase: Client = create_client(url, key)

# Fetch current state
response = supabase.table('winners_payload').select('*').eq('year', 2026).execute()

if response.data and len(response.data) > 0:
    payload = response.data[0]['payload']
    sections = payload.get('sections', [])
    
    print(f"\nCurrent state: {len(sections)} sections\n")
    
    for idx, section in enumerate(sections, 1):
        title = section.get('title', 'Unknown')
        categories = section.get('categories', [])
        total_items = sum(len(cat.get('items', [])) for cat in categories)
        
        print(f"{idx}. {title}")
        print(f"   Categories: {len(categories)}, Total items: {total_items}")
        
        for cat_idx, cat in enumerate(categories, 1):
            cat_title = cat.get('title', 'Unknown')
            items = cat.get('items', [])
            print(f"   {cat_idx}. {cat_title} ({len(items)} items):")
            for item_idx, item in enumerate(items, 1):
                item_title = item.get('title', 'Unknown')
                url = item.get('url', 'No URL')
                print(f"      {item_idx}. {item_title}")
                print(f"         URL: {url}")
        print()
else:
    print("No data found for year 2026")
