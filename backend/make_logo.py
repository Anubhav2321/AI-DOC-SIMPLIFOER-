import os
from PIL import Image, ImageDraw

# --- Configuration ---
# Logo size (Standard for favicons)
size = (64, 64)

# Cyberpunk Theme Colors
cyan_neon = "#00f2ff"   # Bright Blue/Cyan
purple_neon = "#bd00ff" # Bright Purple
dark_bg = "#0a0a0a"     # Dark Background (Pupil)

# 1. Create a blank transparent image
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 2. Draw Outer Eye Shape (Cyan Border)
# Bounding box: [x0, y0, x1, y1]
draw.ellipse([(4, 18), (60, 46)], outline=cyan_neon, width=3)

# 3. Draw Iris (Purple Border with Dark Fill)
draw.ellipse([(22, 22), (42, 42)], fill=dark_bg, outline=purple_neon, width=2)

# 4. Draw Pupil (Solid Cyan Center)
draw.ellipse([(28, 28), (36, 36)], fill=cyan_neon)

# 5. Add a "Digital Glint" (White Sparkle)
draw.line([(38, 24), (42, 20)], fill="white", width=2)

# --- Save the File ---
# Find the 'frontend' folder path
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, 'frontend')

# Ensure frontend directory exists
os.makedirs(frontend_dir, exist_ok=True)

# Define save path
save_path = os.path.join(frontend_dir, 'favicon.png')

# Save the image
img.save(save_path, "PNG")

print("-" * 40)
print("✅ SUCCESS!")
print(f"Logo created at: {save_path}")
print("-" * 40)