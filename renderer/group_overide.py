#group overdirve class
import pygame
class CustomGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            # Call the sprite's custom draw method if it exists,
            # fallback to blit image if not.
            if hasattr(sprite, 'draw'):
                sprite.draw(surface)
            else:
                surface.blit(sprite.image, sprite.rect)