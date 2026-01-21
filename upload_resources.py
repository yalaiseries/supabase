"""Upload resources to Supabase database"""
import json
import requests
import os

# Read resources data
resources_file = 'data/resources-complete.json'
if not os.path.exists(resources_file):
    print(f"Error: {resources_file} not found")
    exit(1)

with open(resources_file, 'r', encoding='utf-8') as f:
    resources_data = json.load(f)

print(f"Uploading resources for year {resources_data['year']}...")

# Upload to Supabase via winners-admin endpoint
response = requests.post(
    'https://xcctqbamimafkkamuwly.supabase.co/functions/v1/winners-admin',
    headers={
        'Content-Type': 'application/json; charset=utf-8',
        'x-admin-token': 'MySecureToken2025!'
    },
    json=resources_data
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print("\n✓ Resources uploaded successfully!")
else:
    print(f"\n✗ Upload failed with status {response.status_code}")
