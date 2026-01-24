#!/usr/bin/env python3
"""Split 2024 'AI Programme Winners' into 'Top Winners' and 'Merit Prizes' categories"""

import os
import json
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def main():
    if not SUPABASE_KEY:
        print("❌ Error: SUPABASE_SERVICE_ROLE_KEY environment variable not set")
        print("   Please set it first with: $env:SUPABASE_SERVICE_ROLE_KEY='your-key'")
        return
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Load the prepared JSON payload
    with open('2024_updated_payload.json', 'r', encoding='utf-8') as f:
        new_payload = json.load(f)
    
    # Fetch 2024 record ID
    response = supabase.table('winners_payload').select('id').eq('year', 2024).execute()
    
    if not response.data:
        print("❌ No 2024 data found")
        return
    
    record_id = response.data[0]['id']
    
    # Update the record with new structure
    update_response = supabase.table('winners_payload').update({
        'payload': new_payload
    }).eq('id', record_id).execute()
    
    print(f"✓ Successfully updated 2024 structure:")
    for cat in new_payload['categories']:
        print(f"  - {cat['category']}: {len(cat.get('useCases', []))} use cases")
    
    # Verify the update
    verify = supabase.table('winners_payload').select('year, payload').eq('year', 2024).execute()
    if verify.data:
        print(f"\n✓ Verified in database:")
        for cat in verify.data[0]['payload']['categories']:
            print(f"  - {cat['category']}: {len(cat.get('useCases', []))} items")

if __name__ == "__main__":
    main()
