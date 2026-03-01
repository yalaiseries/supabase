"""Check all items in Section 5"""
import requests
import os
import json

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SERVICE_ROLE_KEY:
    print("Set SERVICE_ROLE_KEY")
    exit(1)

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
}

response = requests.get(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026&select=*",
    headers=headers
)

rows = response.json()
section_5 = rows[0]['payload']['sections'][4]

print(f"Section 5: {section_5.get('title')}\n")
for i, cat in enumerate(section_5.get('categories', [])):
    cat_name = cat.get('name', f'Category {i+1}')
    print(f"\n{cat_name}:")
    for j, item in enumerate(cat.get('items', [])):
        print(f"  {j+1}. {item.get('name')} - {item.get('desc', '')[:60]}")
