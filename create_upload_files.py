import json

# Read the updated winners files
with open('data/winners-2024-corrected.json', 'r', encoding='utf-8') as f:
    winners_2024 = json.load(f)

with open('data/winners-2025-corrected.json', 'r', encoding='utf-8') as f:
    winners_2025 = json.load(f)

# Create upload payloads
upload_2024 = {
    "year": 2024,
    "payload": winners_2024
}

upload_2025 = {
    "year": 2025,
    "payload": winners_2025
}

# Save upload files
with open('data/temp-upload-2024.json', 'w', encoding='utf-8') as f:
    json.dump(upload_2024, f, indent=2, ensure_ascii=False)

with open('data/temp-upload-2025.json', 'w', encoding='utf-8') as f:
    json.dump(upload_2025, f, indent=2, ensure_ascii=False)

print("Created temp-upload-2024.json and temp-upload-2025.json")
