from PIL import Image, ImageDraw

# Create a new image with a white background
img = Image.new('RGB', (32, 32), color='white')
draw = ImageDraw.Draw(img)

# Draw a simple game controller icon
draw.rectangle([8, 8, 24, 24], fill='blue')  # Main body
draw.ellipse([10, 10, 16, 16], fill='red')   # Left button
draw.ellipse([16, 10, 22, 16], fill='green') # Right button

# Save as PNG
img.save('favicon.png') 