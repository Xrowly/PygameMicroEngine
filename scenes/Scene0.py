# Scene0.py

import pygame
from system.entities import character, mary, stickfigure
from system.abstract_scene import AbstractScene
from system.GameGlobals import scene_manager
from renderer import Light as light
from renderer.group_overide import CustomGroup
from renderer.UI.button import Button  # Note the capital B for class name
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
from renderer.UI.fancy_text import FancyText
def load_and_scale(path, height):
    img = pygame.image.load(path).convert_alpha()
    width = img.get_width() * (height / img.get_height())
    return pygame.transform.scale(img, (int(width), int(height)))

class Scene0(AbstractScene):
    def __init__(self):
    	self.load()
    def load(self):
        self.character_height = SCREEN_HEIGHT // 4
        self.character_image_path = 'assets/white.png'
        self.fancy=FancyText(font_size=24,font_path="assets/fonts/Creepster_Regular.ttf")
        self.character_img = load_and_scale(self.character_image_path, self.character_height)

        self.bstic_height = self.character_height * 2
        self.bstic_img = load_and_scale('assets/stick.png', self.bstic_height)

        self.yr_height = self.character_height * 2
        self.yr_img = load_and_scale('assets/scream.png', self.yr_height)

        self.player = character.Character(
            image_path=self.character_image_path,
            pos=(SCREEN_WIDTH//2 - self.character_img.get_width()//2, SCREEN_HEIGHT - self.character_height // 2),
            width=self.character_img.get_width(),
            height=self.character_height
        )
        self.mary = mary.Mary(
            image_path='assets/scream.png',
            pos=(SCREEN_WIDTH - SCREEN_WIDTH // 3 - self.bstic_img.get_width() // 2, SCREEN_HEIGHT // 6 - self.bstic_height // 2),
            width=self.yr_img.get_width(),
            height=self.yr_height
        )
        self.stick = stickfigure.stickfigure(
            image_path='assets/stick.png',
            pos=(SCREEN_WIDTH // 2 - self.bstic_img.get_width() // 2, SCREEN_HEIGHT - self.bstic_height * 3 // 2),
            width=self.bstic_img.get_width(),
            height=self.bstic_height
        )

        self.background = pygame.image.load('assets/background.png').convert()
        self.entities = CustomGroup(self.player, self.mary, self.stick)

        # Setup lighting stuff here
        self.light_radius = 32
        self.light_alpha = 90
        self.gradient_steps = 100
        self.overlay_color = (20, 30, 50, 120)

        self.light_mask = light.circle_light_mask(self.light_radius, self.gradient_steps, self.light_alpha)
        self.flash_light = light.SpotLight(display_surface=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.beam_mask = self.flash_light.create_beam(debug=False)
        self.Button = Button(
                color=(200, 200, 200, 250),
                width=150,
                height=50,
                pos=(200, 200),
                text="Click Me",
                font_size=24,
                text_color=(255, 255, 255, 255),  # fully invisible text normal
                hover_color=(0, 0, 0, 220),       # invisible hover bg
                click_color=(0, 0, 0, 250),       # invisible click bg
                hover_text_color=(255, 255, 100, 255),
                click_text_color=(255, 100, 100, 255),
                border_color=(255, 0, 0, 255),          # invisible normal border
                hover_border_color=(255, 255, 0, 80),    # yellow visible hover border
                click_border_color=(255, 100, 100, 255),  # red visible click border
                border_width=4,
                fancy_text=self.fancy,
                click_callback=lambda b: print(f"{b.text} was clicked!")
            )

        self.Button.rect.topleft = (250, 250)  # Position the button
        pygame.draw.rect(self.Button.image, (255, 0, 0), self.Button.image.get_rect(), 1)
    
    def enter(self):
        pass

    def draw_light_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        light_pos = (self.player.rect.centerx - self.light_radius, self.player.rect.centery - self.light_radius)
        fls, flr = self.flash_light.draw(self.beam_mask, pygame.math.Vector2(self.player.rect.center), pygame.Vector2(pygame.mouse.get_pos()))
        overlay.blit(fls, flr, special_flags=pygame.BLEND_RGBA_SUB)
        overlay.blit(self.light_mask,(self.mary.rect.centerx+5,self.mary.rect.centery+10),special_flags=pygame.BLEND_RGBA_SUB)
        self.Button.draw(overlay)
        pygame.draw.rect(overlay, (255, 0, 0), self.Button.rect, 1)
        
        #tnt firecracker
        for proj in self.player.projectiles:
            if hasattr(proj, "fuse"):
                fuse_surf, fuse_rect = proj.fuse()
                overlay.blit(fuse_surf, fuse_rect, special_flags=pygame.BLEND_RGBA_SUB)

        return overlay

    def update(self, dt):
        self.entities.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
        

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.entities.draw(screen)
        self.player.projectiles.draw(screen)
        overlay = self.draw_light_overlay()
        screen.blit(overlay, (0, 0))
        
    def handle_events(self, events):
        """Handle all events"""
        # Convert single event to list if needed (backward compatibility)
        if not isinstance(events, (list, tuple)):
            events = [events]
        
        # Process button events
        self.Button.update(events)
        
        # Add other event handling here as needed
        # For example:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Handle space bar press
                    pass
    def exit(self):
        pass