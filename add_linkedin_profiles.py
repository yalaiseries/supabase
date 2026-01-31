"""
Add LinkedIn profiles to co-leads in 2024 and 2025 winners data
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

# LinkedIn mappings
LINKEDIN_PROFILES_2025 = {
    "Lucas LEE": None,  # NA in data
    "CHONG Wen Jin": "linkedin.com/in/wen-jin-chong-42999549",
    "HUANG Ranzi": "linkedin.com/in/ranzi-huang",  # Updated from debug data
    "Ethan OW": "linkedin.com/in/ethanow",
    "CHENG Tai Fatt": "linkedin.com/in/tai-fatt-cheng-a2077833",
    "TAN Tian Chong": "linkedin.com/in/tian-chong-tan-37b16779"
}

LINKEDIN_PROFILES_2024 = {
    "CHONG Wen Jin": "linkedin.com/in/wen-jin-chong-42999549",
    "Bob LEE": "linkedin.com/in/bob-lee-yx-396a75211",
    "Darren TAN": "linkedin.com/in/tanshaohong",
    "Anders Ang Wei Li": "linkedin.com/in/anders-ang",
    "Atenn NEOH": "linkedin.com/in/atenn-neoh",
    "Naomi Marcelle BACHTIAR": "linkedin.com/in/naomi-bachtiar",
    "Gyanish Kakati": "linkedin.com/in/gyanishkakati"
}

def update_linkedin_profiles():
    """Add LinkedIn profiles to winners data"""
    
    print("Updating LinkedIn profiles for 2024 and 2025 winners...")
    
    # Update 2025
    response_2025 = supabase.table("winners_payload").select("*").eq("year", 2025).execute()
    
    if response_2025.data and len(response_2025.data) > 0:
        record_2025 = response_2025.data[0]
        payload_2025 = record_2025['payload']
        
        updated_count_2025 = 0
        
        # Iterate through categories and useCases
        if 'categories' in payload_2025:
            for category in payload_2025['categories']:
                if 'useCases' in category:
                    for use_case in category['useCases']:
                        if 'people' in use_case and use_case['people']:
                            people = use_case['people']
                            
                            # Update lead
                            if 'lead' in people and people['lead']:
                                if isinstance(people['lead'], str):
                                    lead_name = people['lead']
                                    if lead_name in LINKEDIN_PROFILES_2025 and LINKEDIN_PROFILES_2025[lead_name]:
                                        people['lead'] = {
                                            'name': lead_name,
                                            'linkedin': LINKEDIN_PROFILES_2025[lead_name]
                                        }
                                        updated_count_2025 += 1
                                        print(f"  ✓ 2025 - Added LinkedIn for lead: {lead_name}")
                                elif isinstance(people['lead'], dict):
                                    lead_name = people['lead'].get('name', '')
                                    if lead_name in LINKEDIN_PROFILES_2025 and LINKEDIN_PROFILES_2025[lead_name]:
                                        if 'linkedin' not in people['lead']:
                                            people['lead']['linkedin'] = LINKEDIN_PROFILES_2025[lead_name]
                                            updated_count_2025 += 1
                                            print(f"  ✓ 2025 - Added LinkedIn for lead: {lead_name}")
                            
                            # Update co-leads
                            if 'coLeads' in people and isinstance(people['coLeads'], list):
                                for i, co_lead in enumerate(people['coLeads']):
                                    if isinstance(co_lead, str):
                                        co_lead_name = co_lead
                                        if co_lead_name in LINKEDIN_PROFILES_2025 and LINKEDIN_PROFILES_2025[co_lead_name]:
                                            people['coLeads'][i] = {
                                                'name': co_lead_name,
                                                'linkedin': LINKEDIN_PROFILES_2025[co_lead_name]
                                            }
                                            updated_count_2025 += 1
                                            print(f"  ✓ 2025 - Added LinkedIn for co-lead: {co_lead_name}")
                                    elif isinstance(co_lead, dict):
                                        co_lead_name = co_lead.get('name', '')
                                        if co_lead_name in LINKEDIN_PROFILES_2025 and LINKEDIN_PROFILES_2025[co_lead_name]:
                                            if 'linkedin' not in co_lead:
                                                co_lead['linkedin'] = LINKEDIN_PROFILES_2025[co_lead_name]
                                                updated_count_2025 += 1
                                                print(f"  ✓ 2025 - Added LinkedIn for co-lead: {co_lead_name}")
        
        # Update database
        if updated_count_2025 > 0:
            update_response = supabase.table("winners_payload").update({
                "payload": payload_2025
            }).eq("year", 2025).execute()
            
            if update_response.data:
                print(f"\n✅ 2025: Updated {updated_count_2025} LinkedIn profiles")
            else:
                print(f"\n❌ 2025: Failed to update database")
        else:
            print("\n⚠️  2025: No LinkedIn profiles to update")
    
    # Update 2024
    response_2024 = supabase.table("winners_payload").select("*").eq("year", 2024).execute()
    
    if response_2024.data and len(response_2024.data) > 0:
        record_2024 = response_2024.data[0]
        payload_2024 = record_2024['payload']
        
        updated_count_2024 = 0
        
        # Iterate through categories and useCases
        if 'categories' in payload_2024:
            for category in payload_2024['categories']:
                if 'useCases' in category:
                    for use_case in category['useCases']:
                        if 'people' in use_case and use_case['people']:
                            people = use_case['people']
                            
                            # Update lead
                            if 'lead' in people and people['lead']:
                                if isinstance(people['lead'], str):
                                    lead_name = people['lead']
                                    if lead_name in LINKEDIN_PROFILES_2024 and LINKEDIN_PROFILES_2024[lead_name]:
                                        people['lead'] = {
                                            'name': lead_name,
                                            'linkedin': LINKEDIN_PROFILES_2024[lead_name]
                                        }
                                        updated_count_2024 += 1
                                        print(f"  ✓ 2024 - Added LinkedIn for lead: {lead_name}")
                                elif isinstance(people['lead'], dict):
                                    lead_name = people['lead'].get('name', '')
                                    if lead_name in LINKEDIN_PROFILES_2024 and LINKEDIN_PROFILES_2024[lead_name]:
                                        if 'linkedin' not in people['lead']:
                                            people['lead']['linkedin'] = LINKEDIN_PROFILES_2024[lead_name]
                                            updated_count_2024 += 1
                                            print(f"  ✓ 2024 - Added LinkedIn for lead: {lead_name}")
                            
                            # Update co-leads
                            if 'coLeads' in people and isinstance(people['coLeads'], list):
                                for i, co_lead in enumerate(people['coLeads']):
                                    if isinstance(co_lead, str):
                                        co_lead_name = co_lead
                                        if co_lead_name in LINKEDIN_PROFILES_2024 and LINKEDIN_PROFILES_2024[co_lead_name]:
                                            people['coLeads'][i] = {
                                                'name': co_lead_name,
                                                'linkedin': LINKEDIN_PROFILES_2024[co_lead_name]
                                            }
                                            updated_count_2024 += 1
                                            print(f"  ✓ 2024 - Added LinkedIn for co-lead: {co_lead_name}")
                                    elif isinstance(co_lead, dict):
                                        co_lead_name = co_lead.get('name', '')
                                        if co_lead_name in LINKEDIN_PROFILES_2024 and LINKEDIN_PROFILES_2024[co_lead_name]:
                                            if 'linkedin' not in co_lead:
                                                co_lead['linkedin'] = LINKEDIN_PROFILES_2024[co_lead_name]
                                                updated_count_2024 += 1
                                                print(f"  ✓ 2024 - Added LinkedIn for co-lead: {co_lead_name}")
        
        # Update database
        if updated_count_2024 > 0:
            update_response = supabase.table("winners_payload").update({
                "payload": payload_2024
            }).eq("year", 2024).execute()
            
            if update_response.data:
                print(f"\n✅ 2024: Updated {updated_count_2024} LinkedIn profiles")
            else:
                print(f"\n❌ 2024: Failed to update database")
        else:
            print("\n⚠️  2024: No LinkedIn profiles to update")

if __name__ == "__main__":
    update_linkedin_profiles()
