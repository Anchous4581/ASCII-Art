# scene.py
import pygame
from ascii_render import *
from data import char_list, image, font

class Scene:
    def __init__(self, screen):
        self.screen = screen

        self.info = get_image_size(image)
        self.resized = resize_image(image, 200)
        self.image_pixels = list(get_image_pixels(self.resized))

    def update(self, dt):
        brightness = [
            formula_rgb_to_brightness(pixel.r, pixel.g, pixel.b)
            for pixel in self.image_pixels
        ]

        self.index = brightness_to_index(brightness, char_list)
        self.char_text = brightness_to_ascii(self.index, self.resized, char_list)

        print(self.index)

        self.ascii_surface = render_ascii_to_surface(
            self.char_text,
            font_name=font,
            font_size=10,
            font_color=(255, 255, 255),
            bg_color=(0, 0, 0),
        )

        save_surface_as_image(self.ascii_surface, "result/ASCII-image.png")

    def draw(self):
        surface = self.screen.virtual_surface
        surface.fill((30, 30, 30))  # фон

        surface.blit(self.resized, (0, 0))  # отрисовка изображения
        surface.blit(self.ascii_surface, (0, 0))  # отрисовка ASCII текста