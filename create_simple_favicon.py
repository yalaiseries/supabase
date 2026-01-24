#!/usr/bin/env python3
"""Create simple, bold AI favicon that's readable at small sizes"""
from PIL import Image, ImageDraw, ImageFont

# Create 64x64 image with white background
size = 64
img = Image.new('RGB', (size, size), 'white')
draw = ImageDraw.Draw(img)

# Draw orange background
bg_color = '#ff6b35'  # Orange
draw.rectangle([0, 0, size, size], fill=bg_color)

# Draw bold "AI" text
try:
    # Try to use a bold system font
    font = ImageFont.truetype("arial.ttf", 40)
except:
    font = ImageFont.load_default()

text = "AI"
# Get text bbox for centering
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = (size - text_width) // 2
y = (size - text_height) // 2 - 5  # Adjust vertical position

# Draw white text
draw.text((x, y), text, fill='white', font=font)

# Save as PNG
img.save('favicon_simple.png', 'PNG', optimize=True)

print(f"✅ Created simple AI favicon (64x64)")
print(f"   File size: {len(open('favicon_simple.png', 'rb').read())} bytes")
