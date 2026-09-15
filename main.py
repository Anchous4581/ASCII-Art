# main.py
import pygame
from screen import Display
from scene import Scene

pygame.init()

def main():
    running = True
    clock = pygame.time.Clock()

    screen = Display(virtual_size=(1280, 720))
    scene = Scene(screen)

    while running:
        # чтобы при разных фпс игра шла с одинаковой скоростью
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen.resize(event.w, event.h) 

        screen.clear()

        scene.update(dt)
        scene.draw()

        screen.update()

if __name__ == "__main__":
    main()