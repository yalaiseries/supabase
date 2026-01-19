import json
import requests

# Upload 2025 winners
with open('data/temp-2025-restore.json', 'r', encoding='utf-8-sig') as f:
    winners_2025 = f.read()

response = requests.post(
    'https://xcctqbamimafkkamuwly.supabase.co/functions/v1/winners-admin',
    headers={'Content-Type': 'application/json; charset=utf-8', 'x-admin-token': 'MySecureToken2025!'},
    data=winners_2025.encode('utf-8')
)
print(f"2025 Winners upload: {response.status_code} - {response.text}")

# Upload resources with year 9999
with open('data/resources-complete.json', 'r', encoding='utf-8-sig') as f:
    resources = f.read()

response = requests.post(
    'https://xcctqbamimafkkamuwly.supabase.co/functions/v1/winners-admin',
    headers={'Content-Type': 'application/json; charset=utf-8', 'x-admin-token': 'MySecureToken2025!'},
    data=resources.encode('utf-8')
)
print(f"Resources upload: {response.status_code} - {response.text}")
