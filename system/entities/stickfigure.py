import pygame
class stickfigure(pygame.sprite.Sprite):
    def __init__(self, image_path, pos=(0, 0), width=None, height=None):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()

        if width and height:
            self.image = pygame.transform.smoothscale(self.image, (width, height))

        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.Vector2(0, 0)

        # Movement parameters
        self.speed = 5

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    def update(self, dt, screen_width, screen_height):
        
        # Clamp inside screen
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def animation(self):
        pass