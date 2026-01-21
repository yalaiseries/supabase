"""Upload updated winners data to Supabase database"""
import json
import requests

# Read and upload 2024 winners
with open('data/winners-2024.json', 'r', encoding='utf-8') as f:
    winners_2024 = json.load(f)

response = requests.post(
    'https://xcctqbamimafkkamuwly.supabase.co/functions/v1/winners-admin',
    headers={
        'Content-Type': 'application/json; charset=utf-8',
        'x-admin-token': 'MySecureToken2025!'
    },
    json=winners_2024
)

print(f"2024 Winners upload: {response.status_code}")
if response.status_code == 200:
    print(f"✓ 2024 Winners uploaded successfully")
else:
    print(f"Response: {response.text}")

# Read and upload 2025 winners
with open('data/winners-2025.json', 'r', encoding='utf-8') as f:
    winners_2025 = json.load(f)

response = requests.post(
    'https://xcctqbamimafkkamuwly.supabase.co/functions/v1/winners-admin',
    headers={
        'Content-Type': 'application/json; charset=utf-8',
        'x-admin-token': 'MySecureToken2025!'
    },
    json=winners_2025
)

print(f"2025 Winners upload: {response.status_code}")
if response.status_code == 200:
    print(f"✓ 2025 Winners uploaded successfully")
else:
    print(f"Response: {response.text}")
