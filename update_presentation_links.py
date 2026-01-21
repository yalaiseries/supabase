"""
Update winners data to use GitHub-hosted presentation PDFs
"""
import json
from pathlib import Path

# Base URL for raw GitHub files
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/yalaiseries/supabase/main/data/Presentations"

# Directories
data_dir = Path(r"C:\2026_AI_Collaboration\aiseries\data")

def map_presentation_to_usecase(filename: str, year: int) -> tuple:
    """Map presentation filename to usecase position"""
    
    if year == 2025:
        mapping = {
            "2025_Presentation_1_Prize.pdf": ("Top Winners", 0),
            "2025_Presentation_2_Prize.pdf": ("Top Winners", 1),
            "2025_Presentation_3a_Prize.pdf": ("Top Winners", 2),
            "2025_Presentation_3b_Prize.pdf": ("Top Winners", 2),  # Same position, additional link
            "2025_Presentation_Inno1_Prize.pdf": ("Innovation Awards", 0),
            "2025_Presentation_Inno2_Prize.pdf": ("Innovation Awards", 1),
            "2025_Presentation_Inno3_Prize.pdf": ("Innovation Awards", 2),
        }
    elif year == 2024:
        mapping = {
            "2024_Presentation_1_Prize.pdf": ("AI Programme Winners", 0),
            "2024_Presentation_2_Prize.pdf": ("AI Programme Winners", 1),
            "2024_Presentation_3_Prize.pdf": ("AI Programme Winners", 2),
            "2024_Presentation_Merit_1_Prize.pdf": ("AI Programme Winners", 3),
            "2024_Presentation_Merit_2_Prize.pdf": ("AI Programme Winners", 4),
            "2024_Presentation_Merit_3_Prize.pdf": ("AI Programme Winners", 5),
            "2024_Presentation_Merit_4_Prize.pdf": ("AI Programme Winners", 6),
        }
    else:
        return None, None
    
    return mapping.get(filename, (None, None))

def update_winners_data(year: int, presentation_files: list):
    """Update winners JSON file with GitHub URLs for presentations"""
    winners_file = data_dir / f"winners-{year}.json"
    
    print(f"\nUpdating {winners_file.name}...")
    
    with open(winners_file, 'r', encoding='utf-8') as f:
        winners_data = json.load(f)
    
    # Update links in the appropriate useCases
    for filename in presentation_files:
        url = f"{GITHUB_RAW_BASE}/{filename}"
        category_name, position = map_presentation_to_usecase(filename, year)
        
        if category_name and position is not None:
            # Find the category
            for category in winners_data.get("categories", []):
                if category.get("category") == category_name:
                    use_cases = category.get("useCases", [])
                    if position < len(use_cases):
                        # Update or create links array
                        if "links" not in use_cases[position]:
                            use_cases[position]["links"] = []
                        
                        # Check if this is a 3b case (second link for same position)
                        if "3b" in filename:
                            # Add as additional link
                            use_cases[position]["links"].append({
                                "label": "Slides (Part 2)",
                                "url": url
                            })
                            print(f"  ✓ Added {category_name} - Position {position + 1} - Part 2")
                        else:
                            # Replace first "Slides" link or add new one
                            slides_link_found = False
                            for link in use_cases[position]["links"]:
                                if link.get("label") in ["Slides", "Slides (Part 1)"]:
                                    link["url"] = url
                                    if "3a" in filename:
                                        link["label"] = "Slides (Part 1)"
                                    slides_link_found = True
                                    break
                            
                            if not slides_link_found:
                                use_cases[position]["links"].insert(0, {
                                    "label": "Slides (Part 1)" if "3a" in filename else "Slides",
                                    "url": url
                                })
                            
                            print(f"  ✓ Updated {category_name} - Position {position + 1}")
                    break
    
    # Save updated file
    with open(winners_file, 'w', encoding='utf-8') as f:
        json.dump(winners_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Saved {winners_file.name}")

def main():
    print("=" * 70)
    print("Updating Winners Data with GitHub-hosted Presentation Links")
    print("=" * 70)
    
    # Define presentation files
    presentations_2024 = [
        "2024_Presentation_1_Prize.pdf",
        "2024_Presentation_2_Prize.pdf",
        "2024_Presentation_3_Prize.pdf",
        "2024_Presentation_Merit_1_Prize.pdf",
        "2024_Presentation_Merit_2_Prize.pdf",
        "2024_Presentation_Merit_3_Prize.pdf",
        "2024_Presentation_Merit_4_Prize.pdf",
    ]
    
    presentations_2025 = [
        "2025_Presentation_1_Prize.pdf",
        "2025_Presentation_2_Prize.pdf",
        "2025_Presentation_3a_Prize.pdf",
        "2025_Presentation_3b_Prize.pdf",
        "2025_Presentation_Inno1_Prize.pdf",
        "2025_Presentation_Inno2_Prize.pdf",
        "2025_Presentation_Inno3_Prize.pdf",
    ]
    
    # Update winners data files
    update_winners_data(2024, presentations_2024)
    update_winners_data(2025, presentations_2025)
    
    print("\n" + "=" * 70)
    print("✓ All winners data updated with GitHub presentation links!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Commit and push the changes to GitHub")
    print("2. The PDFs in data/Presentations will be accessible via GitHub raw URLs")
    print(f"3. Base URL: {GITHUB_RAW_BASE}")

if __name__ == "__main__":
    main()
