# ascii_render.py
import pygame

def load_image(path):
    return pygame.image.load(path).convert_alpha()

def get_image_size(image):
    return image.get_width(), image.get_height()

def get_image_pixels(image):
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            yield image.get_at((x, y))

def formula_rgb_to_brightness(r, g, b):
    # Преобразуем RGB в яркость (0-255)
    return int(0.299 * r + 0.587 * g + 0.114 * b)

def brightness_to_index(brightness, char_list):
    min_brightness = min(brightness)
    max_brightness = max(brightness)

    index = [
        int(
            (b - min_brightness)
            / (max_brightness - min_brightness)
            * (len(char_list) - 1)
        )
        for b in brightness
    ]

    return index

def brightness_to_ascii(index, image, char_list):
    width, height = get_image_size(image)
    ascii_image = []
    for y in range(height):
        line = ""
        for x in range(width):
            idx = index[y * width + x]
            line += char_list[idx]
        ascii_image.append(line)
    return ascii_image

def render_ascii_to_surface(ascii_image, font_name="Courier New", font_size=10, font_color=(255, 255, 255), bg_color=(0, 0, 0)):
    font = pygame.font.SysFont(font_name, font_size)
    line_height = font.get_linesize()
    surface_width = max(font.size(line)[0] for line in ascii_image)
    surface_height = line_height * len(ascii_image)

    surface = pygame.Surface((surface_width, surface_height))
    surface.fill(bg_color)

    for i, line in enumerate(ascii_image):
        text_surface = font.render(line, True, font_color)
        surface.blit(text_surface, (0, i * line_height))

    return surface

def resize_image(image, target_width):
    orig_width, orig_height = image.get_size()

    aspect_ratio = orig_height / orig_width
    target_height = int(target_width * aspect_ratio * 0.5)
    
    return pygame.transform.scale(image, (target_width, target_height))

def save_surface_as_image(surface, path):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pygame.image.save(surface, path)
