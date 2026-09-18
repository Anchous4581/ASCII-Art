# image.py
from PIL import Image

def load_image(path):
    return Image.open(path).convert("RGB")

def resize_image(image, target_width):
    original_width, original_height = image.size

    aspect_ratio = original_height / original_width
    target_height = int(target_width * aspect_ratio * 1.17)

    return image.resize((target_width, target_height))