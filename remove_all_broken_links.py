"""Remove all broken links from year 2026 resources"""
import requests
import os

SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SERVICE_ROLE_KEY:
    print("Set SERVICE_ROLE_KEY")
    exit(1)

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# List of broken links to remove (based on check results)
broken_urls = [
    "https://asiasociety.org/policy-institute/raising-standards-data-ai-southeast-asia/ai/indonesia",
    "https://www.hbtlaw.com/insights/2024-02/ethical-guidelines-use-artificial-intelligence-ai-indonesia",
    "https://asiasociety.org/policy-institute/raising-standards-data-ai-southeast-asia/ai/thailand",
    "https://mastic.mosti.gov.my/publication/the-national-guidelines-on-ai-governance-ethics/",
    "https://hiverlab.com/dbkl-ai-and-digital-twin-build-for-smarter-malaysia/",
    "https://smythos.com/",
    "https://www.make.com/",
    "https://openart.ai/workflows/bananasss/vid2vid-dance/KpkvqxEsgJbqN5M1jJJg",
    "https://civitai.com/models/618069",
    "https://stablediffusionweb.com/",
    "https://www.midjourney.com/",
    "https://openai.com/index/dall-e-3/",
    "https://unstable.ai/",
    "https://www.krea.ai/apps/realtime/video",
    "https://www.autodesk.com/forma",
    "https://www.autodesk.com/blogs/aec/2025/12/08/shaping-the-future-of-your-agentic-ai-partner/?us_oa=dotcom-us&us_si=8cab143e-8957-4635-ac03-77cba6337608&us_st=agentic%20ai",
    "https://www.autodesk.com/solutions/generative-design",
    "https://www.autodesk.com/solutions/generative-design/architecture-engineering-construction",
]

print("Fetching year 2026 data...")
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026&select=*",
    headers=headers
)

rows = response.json()
payload = rows[0]['payload']
sections = payload['sections']

removed_count = 0

for section in sections:
    for category in section.get('categories', []):
        original_count = len(category['items'])
        category['items'] = [
            item for item in category['items']
            if item.get('url') not in broken_urls
        ]
        removed = original_count - len(category['items'])
        if removed > 0:
            removed_count += removed
            print(f"Removed {removed} broken link(s) from: {section.get('title')}")

payload['sections'] = sections

print(f"\nTotal broken links removed: {removed_count}")
print("\nUpdating database...")

update_response = requests.patch(
    f"{SUPABASE_URL}/rest/v1/winners_payload?year=eq.2026",
    headers=headers,
    json={"payload": payload, "updated_at": "now()"}
)

if update_response.status_code in [200, 204]:
    print(f"SUCCESS! Removed {removed_count} broken links")
    print(f"Remaining working links: {132 - removed_count}")
else:
    print(f"Failed: {update_response.status_code}")
    print(update_response.text)
