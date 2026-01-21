"""
Upload presentation PDFs to Supabase Storage and update winners data
"""
import os
import json
from pathlib import Path
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://xcctqbamimafkkamuwly.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjY3RxYmFtaW1hZmtrYW11d2x5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY1ODMyODUsImV4cCI6MjA1MjE1OTI4NX0.yBOGSEbsQbjZHO7BKMVnUlKmNMmvkp1o3r-QpETn_Zo"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Directories
presentations_dir = Path(r"C:\2026_AI_Collaboration\aiseries\data\Presentations")
data_dir = Path(r"C:\2026_AI_Collaboration\aiseries\data")

# Storage bucket name
BUCKET_NAME = "presentations"

def create_bucket_if_not_exists():
    """Create the presentations bucket if it doesn't exist"""
    try:
        buckets = supabase.storage.list_buckets()
        bucket_exists = any(b.name == BUCKET_NAME for b in buckets)
        
        if not bucket_exists:
            print(f"Creating bucket '{BUCKET_NAME}'...")
            supabase.storage.create_bucket(
                BUCKET_NAME,
                options={"public": True}
            )
            print(f"✓ Bucket '{BUCKET_NAME}' created")
        else:
            print(f"✓ Bucket '{BUCKET_NAME}' already exists")
    except Exception as e:
        print(f"Note: {e}")

def upload_pdf(file_path: Path) -> str:
    """Upload a PDF to Supabase Storage and return the public URL"""
    try:
        # Read file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Upload to Supabase Storage
        file_name = file_path.name
        storage_path = f"{file_name}"
        
        print(f"Uploading {file_name}...")
        
        # Try to remove existing file first
        try:
            supabase.storage.from_(BUCKET_NAME).remove([storage_path])
        except:
            pass
        
        # Upload file
        result = supabase.storage.from_(BUCKET_NAME).upload(
            storage_path,
            file_data,
            file_options={"content-type": "application/pdf"}
        )
        
        # Get public URL
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)
        
        print(f"✓ Uploaded: {public_url}")
        return public_url
        
    except Exception as e:
        print(f"✗ Error uploading {file_path.name}: {e}")
        return None

def map_presentation_to_usecase(filename: str, year: int) -> tuple:
    """Map presentation filename to usecase position"""
    # Extract the identifier from filename
    # 2025_Presentation_1_Prize.pdf -> position 0 (1st in Top Winners)
    # 2025_Presentation_Inno1_Prize.pdf -> position 0 (1st in Innovation Awards)
    
    if year == 2025:
        mapping = {
            "2025_Presentation_1_Prize.pdf": ("Top Winners", 0),
            "2025_Presentation_2_Prize.pdf": ("Top Winners", 1),
            "2025_Presentation_3a_Prize.pdf": ("Top Winners", 2),  # First co-winner
            "2025_Presentation_3b_Prize.pdf": ("Top Winners", 2),  # Same position but different link
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

def update_winners_data(year: int, uploaded_files: dict):
    """Update winners JSON file with new presentation URLs"""
    winners_file = data_dir / f"winners-{year}.json"
    
    with open(winners_file, 'r', encoding='utf-8') as f:
        winners_data = json.load(f)
    
    # Update links in the appropriate useCases
    for filename, url in uploaded_files.items():
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
                        
                        print(f"✓ Updated {year} - {category_name} - Position {position + 1}")
                    break
    
    # Save updated file
    with open(winners_file, 'w', encoding='utf-8') as f:
        json.dump(winners_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved updated {winners_file.name}")

def main():
    print("=" * 60)
    print("Uploading Presentations to Supabase Storage")
    print("=" * 60)
    
    # Create bucket if needed
    create_bucket_if_not_exists()
    print()
    
    # Get all PDF files
    pdf_files = sorted(presentations_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in Presentations directory")
        return
    
    # Upload all PDFs and collect URLs
    uploaded_2024 = {}
    uploaded_2025 = {}
    
    for pdf_file in pdf_files:
        url = upload_pdf(pdf_file)
        if url:
            if "2024" in pdf_file.name:
                uploaded_2024[pdf_file.name] = url
            elif "2025" in pdf_file.name:
                uploaded_2025[pdf_file.name] = url
    
    print()
    print("=" * 60)
    print("Updating Winners Data Files")
    print("=" * 60)
    
    # Update winners data files
    if uploaded_2024:
        update_winners_data(2024, uploaded_2024)
    
    if uploaded_2025:
        update_winners_data(2025, uploaded_2025)
    
    print()
    print("=" * 60)
    print("✓ All presentations uploaded and data updated!")
    print("=" * 60)

if __name__ == "__main__":
    main()
