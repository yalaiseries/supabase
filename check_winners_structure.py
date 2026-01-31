"""
Check current winners data structure to understand how to add LinkedIn profiles
"""

import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_SERVICE_KEY environment variable not set")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_winners_structure():
    """Check the current structure of winners data"""
    
    print("Fetching 2024 and 2025 winners data...")
    
    # Fetch 2024 data
    response_2024 = supabase.table("winners_payload").select("*").eq("year", 2024).execute()
    
    # Fetch 2025 data
    response_2025 = supabase.table("winners_payload").select("*").eq("year", 2025).execute()
    
    if response_2024.data:
        print("\n=== 2024 Winners Structure ===")
        payload_2024 = response_2024.data[0]['payload']
        
        # Check if there are sections
        if 'sections' in payload_2024:
            print(f"Sections found: {len(payload_2024['sections'])}")
            for i, section in enumerate(payload_2024['sections']):
                print(f"\nSection {i}: {section.get('title', 'No title')}")
                if 'categories' in section:
                    for j, category in enumerate(section['categories']):
                        print(f"  Category {j}: {category.get('subtitle', 'No subtitle')}")
                        if 'items' in category and len(category['items']) > 0:
                            # Show first item structure
                            item = category['items'][0]
                            print(f"    Sample item keys: {item.keys()}")
                            print(f"    Sample item: {item}")
        
        # Check if there are winners directly
        if 'winners' in payload_2024:
            print(f"\nWinners array found: {len(payload_2024['winners'])} entries")
            if len(payload_2024['winners']) > 0:
                print(f"Sample winner keys: {payload_2024['winners'][0].keys()}")
                print(f"Sample winner: {payload_2024['winners'][0]}")
    
    if response_2025.data:
        print("\n=== 2025 Winners Structure ===")
        payload_2025 = response_2025.data[0]['payload']
        
        # Check if there are sections
        if 'sections' in payload_2025:
            print(f"Sections found: {len(payload_2025['sections'])}")
            for i, section in enumerate(payload_2025['sections']):
                print(f"\nSection {i}: {section.get('title', 'No title')}")
                if 'categories' in section:
                    for j, category in enumerate(section['categories']):
                        print(f"  Category {j}: {category.get('subtitle', 'No subtitle')}")
                        if 'items' in category and len(category['items']) > 0:
                            # Show first item structure
                            item = category['items'][0]
                            print(f"    Sample item keys: {item.keys()}")
                            print(f"    Sample item: {item}")
        
        # Check if there are winners directly
        if 'winners' in payload_2025:
            print(f"\nWinners array found: {len(payload_2025['winners'])} entries")
            if len(payload_2025['winners']) > 0:
                print(f"Sample winner keys: {payload_2025['winners'][0].keys()}")
                print(f"Sample winner: {payload_2025['winners'][0]}")

if __name__ == "__main__":
    check_winners_structure()
