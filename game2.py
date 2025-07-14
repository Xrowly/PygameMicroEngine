import pygame
import sys
from system.GameGlobals import scene_manager
from scenes.Scene0 import Scene0
from renderer.FrameRater import FrameRateDisplay

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

framerate_display = FrameRateDisplay()

# Setup initial scene
scene_manager.switch_to(Scene0())

def main():
    running = True
    pause = False
    while running:
        dt = clock.tick(60) / 1000
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_e:
                    pause = not pause
        
        # Pass events list to the scene manager
        scene_manager.handle_events(events)

        if not pause:
            scene_manager.update(dt)
            scene_manager.draw(screen)
            framerate_display.draw(screen, clock)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
