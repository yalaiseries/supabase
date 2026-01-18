"""
Extract 2025 data from transposed XLSX (teams as columns, fields as rows)
"""
import openpyxl
import json

wb = openpyxl.load_workbook(r"C:\2026_AI_Collaboration\aiseries\data\2025_AI_Hackathon_Open_Sharing.xlsx")

categories = []

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    
    print(f"\nSheet: {sheet_name}")
    
    # First row has team names/titles (skip first cell which is "Topic")
    team_headers = []
    for cell in list(ws.rows)[0][1:]:  # Skip first column
        if cell.value:
            team_headers.append(str(cell.value).strip())
    
    print(f"Teams found: {len(team_headers)}")
    
    # Get all rows as a dict with first column as key
    data_by_field = {}
    for row in list(ws.rows)[1:]:  # Skip header row
        field_name = str(row[0].value).strip().lower() if row[0].value else ""
        if field_name:
            values = [str(cell.value).strip() if cell.value and str(cell.value).strip() not in ['None', ''] else "" for cell in row[1:]]
            data_by_field[field_name] = values
    
    print(f"Fields: {list(data_by_field.keys())}")
    
    # Build use cases for each team
    use_cases = []
    for i, title in enumerate(team_headers):
        if not title or title.lower() in ['topic', '']:
            continue
        
        use_case = {"title": title}
        
        # Map fields
        field_mapping = {
            'team': 'team',
            'prize': 'award',
            'one sentence summary of what, why, benefits & how': 'summary',
            'about': 'summary',
            'representative speaker': 'rep',
            'designation': 'designation',
            'rep designation': 'designation',
            'lead': 'lead',
            'co-lead': 'coLeads',
            'team members': 'teamMembers',
            'team member': 'teamMembers',
            'slide': 'slide',
            'other links': 'otherLink',
            'linkedin': 'linkedin'
        }
        
        people = {}
        links = []
        
        for field_key, field_values in data_by_field.items():
            if i >= len(field_values):
                continue
            
            value = field_values[i]
            if not value:
                continue
            
            mapped_key = field_mapping.get(field_key)
            
            if mapped_key == 'team':
                use_case['team'] = value
            elif mapped_key == 'award':
                use_case['award'] = value
            elif mapped_key == 'summary' and 'summary' not in use_case:
                use_case['summary'] = value
            elif mapped_key == 'rep':
                people['representativeSpeaker'] = value
            elif mapped_key == 'designation':
                people['designation'] = value
            elif mapped_key == 'lead':
                people['lead'] = value
            elif mapped_key in ['coLeads', 'teamMembers']:
                # Split by newline or comma
                members = [m.strip() for m in value.replace(',', '\n').split('\n') if m.strip()]
                if members:
                    people[mapped_key] = members
            elif mapped_key == 'slide':
                links.append({"label": "Slides", "url": value})
            elif mapped_key == 'otherLink':
                links.append({"label": "Other link", "url": value})
            elif mapped_key == 'linkedin':
                people['linkedin'] = value
        
        if people:
            use_case['people'] = people
        if links:
            use_case['links'] = links
        
        use_cases.append(use_case)
        print(f"  ✓ {title[:50]}")
    
    if use_cases:
        categories.append({
            "category": sheet_name,
            "useCases": use_cases
        })

output = {
    "year": 2025,
    "categories": categories
}

with open(r"C:\2026_AI_Collaboration\aiseries\data\winners-2025.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved 2025 data: {sum(len(cat['useCases']) for cat in categories)} entries across {len(categories)} categories")
