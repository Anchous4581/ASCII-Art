# renderer.py
from PIL import Image, ImageDraw, ImageFont
from config import default_font


def render_ascii_to_image(
    ascii_image,
    font_size=10,
    font_name=default_font,
    font_color=(255, 255, 255),
    background_color=(0, 0, 0),
):
    font = ImageFont.truetype(font_name, font_size)

    char_width = int(font.getlength("A"))

    bbox = font.getbbox("A")
    print("bbox:", bbox)
    print("font size:", font_size)
    char_height = bbox[3] - bbox[1]

    width = char_width * max(len(line) for line in ascii_image)
    height = char_height * len(ascii_image)

    image = Image.new(
        "RGB",
        (width, height),
        background_color
    )

    draw = ImageDraw.Draw(image)

    for y, line in enumerate(ascii_image):
        draw.text(
            (0, y * char_height),
            line,
            font=font,
            fill=font_color
        )

    for text in ["A", "Ag", "ABC", "|||"]:
        bbox = font.getbbox(text)
        print(text, bbox)

    return image
