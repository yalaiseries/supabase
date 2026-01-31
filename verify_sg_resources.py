#!/usr/bin/env python3
"""
Verify Singapore AI resources in Supabase members_resources table
"""
import os
from supabase import create_client, Client

# Load Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("Fetching all resources from members_resources table...")
try:
    result = supabase.table('members_resources').select('*').order('id').execute()
    
    if not result.data:
        print("❌ No data found in members_resources table!")
    else:
        print(f"\n✅ Found {len(result.data)} resources in table:")
        print("\n" + "="*80)
        for resource in result.data:
            print(f"ID {resource['id']}: {resource['title']}")
            print(f"   URL: {resource['url']}")
            print(f"   Note: {resource.get('note', 'N/A')[:100]}...")
            print("-"*80)
            
except Exception as e:
    print(f"❌ Error fetching data: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()
