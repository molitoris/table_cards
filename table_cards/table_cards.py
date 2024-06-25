import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from utils import get_text_dimensions


inch_per_cm = 2.54


def generate_table_cards(iter):
    """ Generate a folded table card (8.5 cm x 5.5 cm) from a A6 card"""

    # Settings for the image
    dpi = 300
    width, height = (10.5 * dpi / inch_per_cm, 14.8 * dpi / inch_per_cm)  # A6
    
    # Font settings
    font_path = "Quicksand.ttf"  # Path to font
    font_size = 130
    font = ImageFont.truetype(font_path, font_size)

    # Helper line
    line_color = "gray"
    line_width = 1

    # Path to the PNG image
    png_image_path = 'flowers.png'
    # Load the PNG image
    png_image = Image.open(png_image_path)

    # Calculate new size of the PNG image, maintaining aspect ratio
    scale_width = int(6 * dpi / inch_per_cm)  # 6 cm width in pixels
    aspect_ratio = png_image.height / png_image.width
    scale_height = int(scale_width * aspect_ratio)

    # Resize image
    png_image_resized = png_image.resize((scale_width, scale_height), Image.ADAPTIVE)

    # Create directory to save images
    os.makedirs('output_images', exist_ok=True)

    for index, row in iter:
        nachname, vorname = row
        image = Image.new('RGB', (round(width), round(height)), 'white')
        draw = ImageDraw.Draw(image)

        # Paste resized PNG image
        png_x = 0  # Left border
        png_y = int(height) // 2  # Vertical middle
        image.paste(png_image_resized, (png_x, png_y), png_image_resized)

        # Draw lines
        # Horizontal line 1.75 cm from top
        top_line_y = int(1.75 * dpi / inch_per_cm)
        draw.line([(0, top_line_y), (width, top_line_y)], fill=line_color, width=line_width)

        # Horizontal line 1.75 cm from bottom
        bottom_line_y = height - int(1.75 * dpi / 2.54)
        draw.line([(0, bottom_line_y), (width, bottom_line_y)], fill=line_color, width=line_width)

        # Horizontal center line
        line_y = height / 2
        draw.line([(0, line_y), (width, line_y)], fill=line_color, width=line_width)

        # Vertical line 2 cm from right
        right_line_x = width - int(2 * dpi / 2.54)
        draw.line([(right_line_x, 0), (right_line_x, height)], fill=line_color, width=line_width)

        # Calculate text width and height
        text = f"{vorname}"
        text_width, _ = get_text_dimensions(text, font=font)

        # Calculate position
        x = (int)((right_line_x- text_width) /2)  # Vertical centered
        y = (height / 2) + (3 * dpi / 2.54)  # 3cm below horizontal center line

        if x <= 20:
            raise AttributeError(f'Text `{text}` too long (index={index})')

        # Add text
        draw.text((x, y), text, fill="black", font=font)

        # Save the image
        image_path = os.path.join('output_images', f'{index:02d}_{vorname}_{nachname}.jpg')
        image.save(image_path, 'JPEG', quality=95)

        print(f'Image saved: {image_path}')

    print("All images have been created.")


if __name__ == '__main__':
    # Load workbook and select active sheet
    df = pd.read_csv('guestlist.csv', delimiter=';')

    df1 = df.loc[df['apero'] == 0, ['Vorname', 'Nachname']]
    
    generate_table_cards(df1.iterrows())