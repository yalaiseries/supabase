"""
Debug: Print full structure of 2024 and 2025 winners data
"""

import os
import json
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_SERVICE_KEY environment variable not set")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def debug_structure():
    """Print full structure"""
    
    # Fetch 2025 data
    response_2025 = supabase.table("winners_payload").select("*").eq("year", 2025).execute()
    
    if response_2025.data:
        print("=== 2025 Full Payload ===")
        print(json.dumps(response_2025.data[0], indent=2))
    
    # Fetch 2024 data
    response_2024 = supabase.table("winners_payload").select("*").eq("year", 2024).execute()
    
    if response_2024.data:
        print("\n\n=== 2024 Full Payload ===")
        print(json.dumps(response_2024.data[0], indent=2))

if __name__ == "__main__":
    debug_structure()
