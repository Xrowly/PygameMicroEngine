#main character and projectile
import math
import pygame
from physics_engine.tract import projectile
import renderer.Light as light

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, pos=(0, 0), width=None, height=None):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()

        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.Vector2(0, 0)

        # Movement parameters
        self.speed = 5
        # Shooting mechanics
        self.projectiles = pygame.sprite.Group()
        self.last_shot_time = 0
        self.shoot_cooldown = 0.3  # seconds

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    def update(self, dt, screen_width, screen_height):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        # Shoot projectile
        now = pygame.time.get_ticks() / 1000
        if keys[pygame.K_SPACE] and (now - self.last_shot_time) >= self.shoot_cooldown:
            self.last_shot_time = now
            mouse_pos = pygame.mouse.get_pos()
            proj = ProjectileEntity(coords=self.rect.center, speed=640, target_pos=mouse_pos)

            self.projectiles.add(proj)

        # Clamp inside screen
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

        # Update projectiles
        self.projectiles.update(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for proj in self.projectiles:
            proj.draw_trajectory(surface)
        self.projectiles.draw(surface)


    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class ProjectileEntity(pygame.sprite.Sprite):
    def __init__(self, coords, speed, target_pos):
        super().__init__()
        # Calculate angle from coords to target_pos
        dx = target_pos[0] - coords[0]
        dy = target_pos[1] - coords[1]
        angle = math.degrees(math.atan2(dy, dx))  # angle in degrees

        self.traj = projectile(coords, speed, angle, t=0)
        self.image = pygame.image.load('assets/tnt.png').convert_alpha() 
        self.rect = self.image.get_rect(center=coords)
        self.active = True
        self.death_timer = 0

    def update(self, dt):
        if not self.active:
            self.death_timer += dt
            if self.death_timer >= 3:
                self.kill()
            return

        self.traj.update(dt)
        x, y = self.traj.pos
        screen_height = pygame.display.get_surface().get_height()
        if y >= screen_height - 64:
            y = screen_height - 64
            self.active = False

        self.rect.center = (x, y)

    def animation(self):
        pass
    def get_trajectory_points(self, steps=30, step_time=0.1):
        points = []
        for i in range(steps):
            t = self.traj.t + i * step_time
            x, y = self.traj.position_at(t)  # You must have a method like this
            points.append((x, y))
        return points
    def draw_trajectory(self, surface):
        points = self.get_trajectory_points()
        gray = (128, 128, 128)
        alpha = 80  # transparency

        for point in points:
            surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*gray, alpha), (3, 3), 3)
            surface.blit(surf, (point[0] - 3, point[1] - 3))

    def fuse(self):
        light_radius = 10
        light_alpha = 100
        gradient_steps = 100

        # Create the glowing fuse effect
        fuse_surf = light.circle_light_mask(light_radius, gradient_steps, light_alpha)
        # Center it on the projectile
        fuse_rect = fuse_surf.get_rect(center=(self.rect.centerx + 16, self.rect.centery - 3))
        return fuse_surf, fuse_rect
