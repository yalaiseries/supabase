"""
Convert AISeriesIcon.png to an embedded SVG favicon
"""
import base64
from pathlib import Path

# Read the PNG file
png_path = Path(r"C:\2026_AI_Collaboration\aiseries\data\AIFavicon.png")
svg_output = Path(r"C:\2026_AI_Collaboration\aiseries\favicon.svg")

with open(png_path, 'rb') as f:
    png_data = f.read()

# Encode to base64
png_base64 = base64.b64encode(png_data).decode('utf-8')

# Create SVG with embedded PNG
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64">
  <image width="64" height="64" xlink:href="data:image/png;base64,{png_base64}"/>
</svg>'''

# Write SVG file
with open(svg_output, 'w') as f:
    f.write(svg_content)

print(f"✓ Created favicon.svg with embedded PNG")
print(f"  SVG file size: {len(svg_content):,} bytes")
print(f"  Original PNG: {len(png_data):,} bytes")
