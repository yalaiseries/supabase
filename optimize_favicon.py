"""
Optimize AISeriesIcon.png to create a proper favicon
Creates multiple sizes for web use
"""

from PIL import Image
import os

# Input and output paths
input_path = r"C:\2026_AI_Collaboration\aiseries\data\AISeriesIcon.png"
output_favicon = r"C:\2026_AI_Collaboration\aiseries\favicon.png"
output_32 = r"C:\2026_AI_Collaboration\aiseries\assets\icon-32.png"
output_192 = r"C:\2026_AI_Collaboration\aiseries\assets\icon-192.png"
output_512 = r"C:\2026_AI_Collaboration\aiseries\assets\icon-512.png"

# Create assets directory if it doesn't exist
os.makedirs(r"C:\2026_AI_Collaboration\aiseries\assets", exist_ok=True)

# Open the original image
print(f"Opening {input_path}...")
img = Image.open(input_path)
print(f"Original size: {img.size}, Mode: {img.mode}, Format: {img.format}")

# Convert to RGBA if needed
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Create 32x32 favicon (standard size)
print("Creating 32x32 favicon...")
favicon_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
favicon_32.save(output_favicon, 'PNG', optimize=True)
favicon_32.save(output_32, 'PNG', optimize=True)
print(f"Saved: {output_favicon}")

# Create 192x192 for web manifest
print("Creating 192x192 icon...")
icon_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
icon_192.save(output_192, 'PNG', optimize=True)
print(f"Saved: {output_192}")

# Create 512x512 for web manifest
print("Creating 512x512 icon...")
icon_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
icon_512.save(output_512, 'PNG', optimize=True)
print(f"Saved: {output_512}")

# Print file sizes
for path in [output_favicon, output_32, output_192, output_512]:
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"{os.path.basename(path)}: {size:,} bytes ({size/1024:.1f} KB)")

print("\nDone! Favicon and icons created successfully.")
