from PIL import ImageFont


def get_text_dimensions(text_string: str, font: ImageFont.FreeTypeFont) -> ():
    """ Calculate size of a text
    """
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)