from PIL import Image, ImageDraw

def create_food():
    # Create a new image with RGBA mode (for transparency)
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    apple_red = (231, 76, 60)  # Bright red
    dark_red = (192, 57, 43)   # Darker red for border
    highlight_color = (255, 255, 255, 76)  # White with 30% opacity
    leaf_green = (46, 204, 113) # Bright green for leaf
    
    # Draw main apple body
    draw.ellipse(
        [(2, 2), (17, 17)],
        fill=apple_red,
        outline=dark_red
    )
    
    # Draw leaf
    points = [
        (9, 2),   # Base of leaf
        (11, 0),  # Tip of leaf
        (13, 2)   # Base of leaf
    ]
    draw.polygon(points, fill=leaf_green)
    
    # Add highlight for 3D effect
    draw.ellipse(
        [(6, 6), (12, 8)],
        fill=highlight_color
    )
    
    # Save the image
    img.save('food.png')

if __name__ == "__main__":
    create_food()