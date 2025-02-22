from PIL import Image, ImageDraw

def create_snake_segment():
    # Create a new image with RGBA mode (for transparency)
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    main_color = (46, 204, 113)  # #2ecc71 in RGB
    border_color = (39, 174, 96)  # #27ae60 in RGB
    highlight_color = (255, 255, 255, 76)  # White with 30% opacity
    
    # Draw main body (slightly smaller to account for border)
    draw.rounded_rectangle(
        [(1, 1), (18, 18)],
        radius=4,
        fill=main_color,
        outline=border_color
    )
    
    # Add highlight for 3D effect
    draw.ellipse(
        [(5, 5), (15, 8)],
        fill=highlight_color
    )
    
    # Save the image
    img.save('snake_segment.png')

if __name__ == "__main__":
    create_snake_segment()