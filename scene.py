# scene.py
import pygame
from ascii_render import load_image, get_image_pixels, formula_rgb_to_brightness, hi, brightness_to_ascii, render_ascii_to_surface

class Scene:
    def __init__(self, screen):
        self.screen = screen

        self.load_image = load_image("data/3.png")
        self.index = []

    def update(self, dt):
        self.image_pixels = list(get_image_pixels(self.load_image))

        brightness = [
            formula_rgb_to_brightness(pixel.r, pixel.g, pixel.b)
            for pixel in self.image_pixels
        ]

        self.index = hi(brightness)
        self.char_text = brightness_to_ascii(self.index, self.load_image)

        # print(brightness)
        # print(self.image_pixels)
        # print(formula_rgb_to_brightness(self.image_pixels[0].r, self.image_pixels[0].g, self.image_pixels[0].b))
        print(self.char_text)
    
    def draw(self):
        surface = self.screen.virtual_surface
        surface.fill((30, 30, 30))  # фон

        surface.blit(self.load_image, (0, 0))  # отрисовка изображения
        surface.blit(render_ascii_to_surface(self.char_text, font_size=10, font_color=(255, 255, 255), bg_color=(0, 0, 0)), (0, 0))  # отрисовка ASCII текста