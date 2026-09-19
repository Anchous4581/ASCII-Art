# converter.py
from .config import char_list, default_width
from .image import load_image, resize_image

def get_brightness(image):
    brightness = []

    for pixel in image.getdata():
        r, g, b = pixel
        brightness.append(formula_rgb_to_brightness(r, g, b))

    return brightness

def formula_rgb_to_brightness(r, g, b):
    # Преобразуем RGB в яркость (0-255)
    return int(0.299 * r + 0.587 * g + 0.114 * b)

def brightness_to_index(brightness, characters):
    min_brightness = min(brightness)
    max_brightness = max(brightness)

    if max_brightness == min_brightness:
        return [0] * len(brightness)

    return [
        int(
            (b - min_brightness)
            / (max_brightness - min_brightness)
            * (int(len(characters) - 1))
        )
        for b in brightness
    ]

def brightness_to_ascii(index, width, height, characters):
    ascii_image = []

    for y in range(height):
        line = ""

        for x in range(width):
            idx = index[y * width + x]
            line += characters[idx]

        ascii_image.append(line)

    return ascii_image


# итогавая функция
def convert(path, target_width=default_width):
    image = load_image(path)
    image = resize_image(image, target_width)

    brightness = get_brightness(image)
    index = brightness_to_index(brightness, char_list)

    width, height = image.size

    return brightness_to_ascii(
        index,
        width,
        height,
        char_list
    )