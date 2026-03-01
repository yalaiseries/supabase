"""Remove duplicate AI at Trimble entries from Section 5"""
import requests
import os

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SERVICE_ROLE_KEY:
    print("Set SERVICE_ROLE_KEY")
    exit(1)

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

print("Fetching year 2026 data...")
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026&select=*",
    headers=headers
)

rows = response.json()
payload = rows[0]['payload']
sections = payload['sections']
section_5 = sections[4]

print(f"Section 5: {section_5.get('title')}\n")

# Remove duplicates from Category 2 (index 1)
cat2 = section_5['categories'][1]
original_count = len(cat2['items'])

# Keep only unique items (first occurrence)
seen_names = set()
unique_items = []
for item in cat2['items']:
    if item['name'] not in seen_names:
        seen_names.add(item['name'])
        unique_items.append(item)

cat2['items'] = unique_items

removed = original_count - len(unique_items)
print(f"Category 2: Removed {removed} duplicate(s)")
print(f"  Before: {original_count} items")
print(f"  After: {len(unique_items)} items\n")

sections[4] = section_5
payload['sections'] = sections

print("Updating database...")
update_response = requests.patch(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026",
    headers=headers,
    json={"payload": payload, "updated_at": "now()"}
)

if update_response.status_code in [200, 204]:
    print("SUCCESS! Removed duplicate AI at Trimble entries")
else:
    print(f"Failed: {update_response.status_code}")
    print(update_response.text)
