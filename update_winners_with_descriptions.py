import json
import pandas as pd

# Read Excel files
df_2024 = pd.read_excel('data/2024.xlsx')
slide_idx_2024 = df_2024[df_2024['Topic'] == 'Slide'].index[0]
summary_idx_2024 = df_2024[df_2024['Topic'] == 'One sentence summary of What, Why, Benefits & How '].index[0]

df_2025 = pd.read_excel('data/2025.xlsx')
slide_idx_2025 = df_2025[df_2025['Topic'] == 'Slide'].index[0]
summary_idx_2025 = df_2025[df_2025['Topic'] == 'One sentence summary of What, Why, Benefits & How '].index[0]

# Create lookup dictionaries
lookup_2024 = {}
for col in df_2024.columns[1:]:
    lookup_2024[col] = {
        'slide': str(df_2024.iloc[slide_idx_2024][col]) if pd.notna(df_2024.iloc[slide_idx_2024][col]) else '',
        'summary': str(df_2024.iloc[summary_idx_2024][col]) if pd.notna(df_2024.iloc[summary_idx_2024][col]) else ''
    }

lookup_2025 = {}
for col in df_2025.columns[1:]:
    lookup_2025[col] = {
        'slide': str(df_2025.iloc[slide_idx_2025][col]) if pd.notna(df_2025.iloc[slide_idx_2025][col]) else '',
        'summary': str(df_2025.iloc[summary_idx_2025][col]) if pd.notna(df_2025.iloc[summary_idx_2025][col]) else ''
    }

# Read existing winners JSON files
with open('data/winners-2024-corrected.json', 'r', encoding='utf-8') as f:
    winners_2024 = json.load(f)

with open('data/winners-2025-corrected.json', 'r', encoding='utf-8') as f:
    winners_2025 = json.load(f)

# Helper function to find matching key
def find_matching_key(title, lookup_dict):
    title_lower = title.lower().strip()
    for key in lookup_dict.keys():
        if title_lower in key.lower() or key.lower() in title_lower:
            return key
    return None

# Update 2024 winners
for category in winners_2024.get('categories', []):
    for useCase in category.get('useCases', []):
        title = useCase.get('title', '')
        team = useCase.get('team', '')
        
        # Try to find match in lookup
        match_key = find_matching_key(title, lookup_2024)
        if not match_key and team:
            match_key = find_matching_key(team, lookup_2024)
        
        if match_key:
            data = lookup_2024[match_key]
            if data['summary']:
                useCase['summary'] = data['summary']
            if data['slide']:
                # Add to links array
                if 'links' not in useCase:
                    useCase['links'] = []
                # Check if slide link already exists
                has_slide = any(link.get('label', '').lower() == 'presentation' for link in useCase['links'])
                if not has_slide:
                    useCase['links'].append({
                        'label': 'Presentation',
                        'url': data['slide']
                    })

# Update 2025 winners
for category in winners_2025.get('categories', []):
    for useCase in category.get('useCases', []):
        title = useCase.get('title', '')
        team = useCase.get('team', '')
        
        # Try to find match in lookup
        match_key = find_matching_key(title, lookup_2025)
        if not match_key and team:
            match_key = find_matching_key(team, lookup_2025)
        
        if match_key:
            data = lookup_2025[match_key]
            if data['summary']:
                useCase['summary'] = data['summary']
            if data['slide']:
                # Add to links array
                if 'links' not in useCase:
                    useCase['links'] = []
                # Check if slide link already exists
                has_slide = any(link.get('label', '').lower() == 'presentation' for link in useCase['links'])
                if not has_slide:
                    useCase['links'].append({
                        'label': 'Presentation',
                        'url': data['slide']
                    })

# Save updated files
with open('data/winners-2024-corrected.json', 'w', encoding='utf-8') as f:
    json.dump(winners_2024, f, indent=2, ensure_ascii=False)

with open('data/winners-2025-corrected.json', 'w', encoding='utf-8') as f:
    json.dump(winners_2025, f, indent=2, ensure_ascii=False)

print("Updated winners-2024-corrected.json and winners-2025-corrected.json with summaries and presentation links")
print("\n2024 matches:")
for category in winners_2024.get('categories', []):
    for useCase in category.get('useCases', []):
        print(f"  - {useCase.get('title')}: {'✓ summary' if useCase.get('summary') else '✗ no summary'}, {'✓ slide' if any(l.get('label')=='Presentation' for l in useCase.get('links', [])) else '✗ no slide'}")

print("\n2025 matches:")
for category in winners_2025.get('categories', []):
    for useCase in category.get('useCases', []):
        print(f"  - {useCase.get('title')}: {'✓ summary' if useCase.get('summary') else '✗ no summary'}, {'✓ slide' if any(l.get('label')=='Presentation' for l in useCase.get('links', [])) else '✗ no slide'}")
