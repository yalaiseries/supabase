"""Extract team data from DOCX by parsing text structure"""
from docx import Document
import json
import re

doc = Document(r"C:\2026_AI_Collaboration\aiseries\data\2024_AI_Programme.docx")

# Look for team headings
teams = []
current_team = {}
current_section = None

for para in doc.paragraphs:
    text = para.text.strip()
    
    if not text:
        continue
    
    # Check if this is a team header (e.g., "Team 1", "Team 2")
    if re.match(r'^Team \d+$', text):
        # Save previous team
        if current_team and 'title' in current_team:
            teams.append(current_team)
        # Start new team
        current_team = {'team': text}
        current_section = None
        continue
    
    # Check for section headers
    if text in ['Problems and Challenges', 'Objectives and Impact', 'Solutions and Tools']:
        current_section = text.lower().replace(' and ', '_').replace(' ', '_')
        continue
    
    # First non-empty line after Team X is the title
    if 'team' in current_team and 'title' not in current_team:
        current_team['title'] = text
        continue
    
    # Collect content under sections
    if current_section and text:
        if current_section not in current_team:
            current_team[current_section] = []
        current_team[current_section].append(text)

# Add last team
if current_team and 'title' in current_team:
    teams.append(current_team)

print(f"Found {len(teams)} teams\n")

for i, team in enumerate(teams, 1):
    print(f"Team {i}: {team.get('title', 'No title')[:60]}")
    print(f"  Team name: {team.get('team', 'N/A')}")
    print(f"  Sections: {', '.join([k for k in team.keys() if k not in ['team', 'title']])}")
    print()

# Save structured data
output = {
    "year": 2024,
    "categories": [
        {
            "category": "AI Programme Winners",
            "useCases": [
                {
                    "title": team.get('title', ''),
                    "team": team.get('team', ''),
                    "summary": ' '.join(team.get('objectives_impact', [''])[:1])[:200] if 'objectives_impact' in team else ''
                }
                for team in teams
            ]
        }
    ]
}

with open(r"C:\2026_AI_Collaboration\aiseries\data\winners-2024.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✓ Saved {len(teams)} teams to winners-2024.json")
