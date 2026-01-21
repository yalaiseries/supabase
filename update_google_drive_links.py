"""
Update winners data with Google Drive presentation links
Removes "Other link" entries and replaces with viewable Google Drive links
"""
import json
from pathlib import Path

data_dir = Path(r"C:\2026_AI_Collaboration\aiseries\data")

# Google Drive links for each presentation
drive_links_2024 = {
    0: "https://drive.google.com/file/d/1aC3FIrdixQvPSTuthVS36ygZIeI4sZu7/view",  # 1st prize
    1: "https://drive.google.com/file/d/11KD1OxkRrmnCnWV7V9PPJPVRDc7el0Ds/view?usp=drive_link",  # 2nd prize
    2: "https://drive.google.com/file/d/1S0K6z3fyTcR6d-KhDQW6ULimUho9uhRT/view?usp=drive_link",  # 3rd prize
    3: "https://drive.google.com/file/d/1UTDL_3hc-uUIrSnE3EzgFdsrjFr1X5Ts/view?usp=drive_link",  # Merit 1
    4: "https://drive.google.com/file/d/1SSpkbOsygsVnrrhjbHuLEGRksByOLxsf/view?usp=drive_link",  # Merit 2
    5: "https://drive.google.com/file/d/1Xe4ohLDOs0HfFBojLXLhJKaLITOCWdgt/view?usp=drive_link",  # Merit 3
    6: "https://drive.google.com/file/d/1kmIm-VD5lQgARPulWFO535VCilyRslo9/view?usp=drive_link",  # Merit 4
}

drive_links_2025 = {
    "top_winners": {
        0: "https://drive.google.com/file/d/10CgeNLzlXUaoeBSWImENZ-6Ky1HtQnSF/view?usp=drive_link",  # 1st
        1: "https://drive.google.com/file/d/1qzu0mVGPPaB-AuOFMIh-82jlbXeV6oux/view?usp=drive_link",  # 2nd
        2: {  # 3rd (two parts)
            "part1": "https://drive.google.com/file/d/19IO2U86orVDmYfy7mOKsdISwQLbVvLgM/view?usp=drive_link",
            "part2": "https://drive.google.com/file/d/1OcY0s1n7_cLjFXKJ2tyjayZCZFW729rB/view?usp=drive_link",
        }
    },
    "innovation_awards": {
        0: "https://drive.google.com/file/d/1u7cMTGcIamOWz5kgPK7sUxvM2Y4CgfBY/view?usp=drive_link",  # Inno 1
        1: "https://drive.google.com/file/d/1Jdu41FVaVX7PQlELRY4PvX9WazjFcpH6/view?usp=drive_link",  # Inno 2
        2: "https://drive.google.com/file/d/1uIreblmXXeVmTaJyq3xSaqQbM7i1A5-3/view?usp=drive_link",  # Inno 3
    }
}

def update_2024_winners():
    """Update 2024 winners with Google Drive links"""
    winners_file = data_dir / "winners-2024.json"
    
    with open(winners_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Updating 2024 winners...")
    
    for category in data.get("categories", []):
        if category.get("category") == "AI Programme Winners":
            use_cases = category.get("useCases", [])
            for idx, use_case in enumerate(use_cases):
                if idx in drive_links_2024:
                    # Replace links array with single Google Drive link
                    use_case["links"] = [{
                        "label": "Slides",
                        "url": drive_links_2024[idx]
                    }]
                    print(f"  ✓ Updated position {idx + 1}")
    
    with open(winners_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {winners_file.name}\n")

def update_2025_winners():
    """Update 2025 winners with Google Drive links"""
    winners_file = data_dir / "winners-2025.json"
    
    with open(winners_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Updating 2025 winners...")
    
    for category in data.get("categories", []):
        category_name = category.get("category")
        use_cases = category.get("useCases", [])
        
        if category_name == "Top Winners":
            for idx, use_case in enumerate(use_cases):
                if idx in drive_links_2025["top_winners"]:
                    link_data = drive_links_2025["top_winners"][idx]
                    
                    if isinstance(link_data, dict):  # 3rd place with two parts
                        use_case["links"] = [
                            {
                                "label": "Slides (Part 1)",
                                "url": link_data["part1"]
                            },
                            {
                                "label": "Slides (Part 2)",
                                "url": link_data["part2"]
                            }
                        ]
                        print(f"  ✓ Updated Top Winners position {idx + 1} (Part 1 & 2)")
                    else:
                        use_case["links"] = [{
                            "label": "Slides",
                            "url": link_data
                        }]
                        print(f"  ✓ Updated Top Winners position {idx + 1}")
        
        elif category_name == "Innovation Awards":
            for idx, use_case in enumerate(use_cases):
                if idx in drive_links_2025["innovation_awards"]:
                    use_case["links"] = [{
                        "label": "Slides",
                        "url": drive_links_2025["innovation_awards"][idx]
                    }]
                    print(f"  ✓ Updated Innovation Awards position {idx + 1}")
    
    with open(winners_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {winners_file.name}\n")

def main():
    print("=" * 70)
    print("Updating Winners with Google Drive Presentation Links")
    print("=" * 70)
    print()
    
    update_2024_winners()
    update_2025_winners()
    
    print("=" * 70)
    print("✓ All winners updated with Google Drive links!")
    print("✓ 'Other link' entries removed")
    print("=" * 70)

if __name__ == "__main__":
    main()
