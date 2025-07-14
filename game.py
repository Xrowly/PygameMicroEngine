import pygame
from renderer import Light as light
from renderer.FrameRater import FrameRateDisplay
from physics_engine.tract import projectile
from system import character, mary, stickfigure
from scenes.Scene0 import Scene0
import sys


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

framerate_display = FrameRateDisplay()
scene0 = Scene0()

def main():
    running = True
    pause = False
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_e:
                    pause = not pause
        if not pause:
            scene0.update(dt)

            scene0.draw(screen)
            framerate_display.draw(screen,clock)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()