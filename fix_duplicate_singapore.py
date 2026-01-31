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

print("Fetching current winners_payload for year 2026...")
response = supabase.table("winners_payload").select("payload").eq("year", 2026).execute()

if not response.data:
    print("ERROR: No data found for year 2026")
    exit(1)

payload = response.data[0]["payload"]
sections = payload.get("sections", [])

print(f"Current sections count: {len(sections)}")

# Find and remove the first Singapore section (Section 1 - the incomplete one)
# Keep Section 2 which has the merged data
filtered_sections = []
singapore_count = 0
for section in sections:
    if "AI Framework & Strategy (Singapore)" in section.get("title", ""):
        singapore_count += 1
        if singapore_count == 1:
            print(f"Removing Section 1 (incomplete): {section.get('title')}")
            continue  # Skip this one
        else:
            print(f"Keeping Section 2 (merged): {section.get('title')}")
    filtered_sections.append(section)

print(f"\nNew sections count: {len(filtered_sections)}")

# Update the payload
new_payload = {
    "sections": filtered_sections
}

print("\nUpdating database...")
update_response = supabase.table("winners_payload").update({"payload": new_payload}).eq("year", 2026).execute()

print("✓ Successfully removed duplicate Singapore section")
print(f"✓ Total sections: {len(filtered_sections)}")
print("✓ Only the merged Singapore section (with 12 items) remains")
