# screen.py
import pygame

class Display:
    def __init__(self, virtual_size=(800, 600)):
        self.v_width, self.v_height = virtual_size

        self.width = self.v_width
        self.height = self.v_height

        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("ASCII Art")

        # виртуальный экран
        self.virtual_surface = pygame.Surface((self.v_width, self.v_height))

    def clear(self, color=(0, 0, 0)):
        self.virtual_surface.fill(color)

    def update(self):
        scaled = pygame.transform.scale(self.virtual_surface, (self.width, self.height))
        self.surface.blit(scaled, (0, 0))
        pygame.display.flip()

    def resize(self, w, h):
        self.width = w
        self.height = h
        self.surface = pygame.display.set_mode((w, h), pygame.RESIZABLE)