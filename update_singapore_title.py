#!/usr/bin/env python3
import os
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

# Update Singapore section title
for section in sections:
    if "AI Framework & Strategy (Singapore)" in section.get("title", ""):
        old_title = section["title"]
        section["title"] = "1. AI Governance, Strategy & Programmes (Singapore)"
        print(f"Updated title:")
        print(f"  From: {old_title}")
        print(f"  To:   {section['title']}")
        break

# Update database
print("\nUpdating database...")
update_response = supabase.table("winners_payload").update({"payload": payload}).eq("year", 2026).execute()

print("✓ Successfully updated section title")
