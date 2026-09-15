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

def hi(brightness, char_list = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]):
    step = len(char_list)
    step_brightness = int(255 / step)

    index = [int(b / step_brightness) for b in brightness]
    return index

def brightness_to_ascii(index, image, char_list=["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]):
    width, height = get_image_size(image)
    ascii_image = []
    for y in range(height):
        line = ""
        for x in range(width):
            idx = index[y * width + x]
            line += char_list[idx]
        ascii_image.append(line)
    return ascii_image

def render_ascii_to_surface(ascii_image, font_size=10, font_color=(255, 255, 255), bg_color=(0, 0, 0)):
    font = pygame.font.SysFont("Courier", font_size)
    line_height = font.get_linesize()
    surface_width = max(font.size(line)[0] for line in ascii_image)
    surface_height = line_height * len(ascii_image)

    surface = pygame.Surface((surface_width, surface_height))
    surface.fill(bg_color)

    for i, line in enumerate(ascii_image):
        text_surface = font.render(line, True, font_color)
        surface.blit(text_surface, (0, i * line_height))

    return surface