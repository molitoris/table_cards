import numpy as np
import pandas as pd

from typing import Tuple

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import red
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def get_heart_coords():
    t = np.linspace(0, 2 * np.pi, 1000)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    # Move origin to lower left corner
    x -= min(x)
    y -= min(y)

    # Scale to width of 1 
    x *= 1 / max(x)
    y *= 1 / max(y)

    return x, y


def grid_on_page(width: float, height: float, page_dim: Tuple[float, float]):
    """ Calculate maximal number of rows and columns on a given page """

    page_width, page_height = page_dim

    rows = int(page_height / height)
    cols = int(page_width / width)

    return rows, cols


if __name__ == '__main__':

    page_paddingX = 1 * cm
    page_paddingY = 0.8 * cm

    # Width of object itself
    obj_width = 4.8 * cm
    obj_height = 4.3 * cm

    # Width between two objects
    obj_paddingX = 0.5 * cm
    obj_paddingY = 0.2 * cm

    page_dim = landscape(A4)

    font_path = './QuicksandBold700.ttf'
    font_name = 'Quicksand Bold'
    font_size = 20

    df = pd.read_csv('guestlist.csv', delimiter=';')

    rows, cols = grid_on_page(width=(obj_width + obj_paddingX), height=(obj_height + obj_paddingY), page_dim=page_dim)
    x, y = get_heart_coords()

    c = canvas.Canvas(f"heart.pdf", pagesize=page_dim)
    c.setStrokeColor(red)
    for index, (lastname, firstname) in df.iterrows():

        # Calculate grid position on page
        col = index % cols
        row = (index % (rows * cols))  // cols

        print(f'Index: {index}, row: {row}, col: {col}')

        pdfmetrics.registerFont(TTFont(font_name, font_path))

        offsetX = page_paddingX + (obj_width + obj_paddingX) * col
        offsetY = page_paddingY + (obj_height + obj_paddingY) * row

        # Calculate current offset
        current_x = x * obj_width + offsetX
        current_y = y * obj_height + offsetY

        # Convert coordinates into a tuples with (x1, y1, x2, y2), ...
        linelist = [(current_x[i], current_y[i], current_x[i+1], current_y[i+1]) for i in range(len(x)-1)]

        # Draw heart shape
        c.lines(linelist)

        # Configure font
        font_size = 18 if len(firstname) > 11 else 22
        c.setFont(font_name, font_size)

        # Calculate width of text
        text_width = pdfmetrics.stringWidth(firstname, font_name, font_size)

        # Add text horizontally centered
        c.drawString((offsetX + obj_width/2) - text_width / 2, (offsetY + 2.5 * cm), firstname)

        if index > 0 and (index + 1) % (cols * rows) == 0:
            print('Next page')
            c.showPage()
            c.setStrokeColor(red)
    
    c.save()
    print(f'Processed {index} elements')

        
    
