# fancy_text.py
import pygame
import os

class FancyText:
    def __init__(self, font=None, font_size=20, font_path=None):
        """
        Initialize FancyText.

        Args:
            font: System font name (ignored if font_path is provided)
            font_size: Font size in points
            font_path: Path to a .ttf/.otf font file (takes priority)
        """
        if font_path and os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.SysFont(font, font_size)

    def render(self, text, text_color=(255, 255, 255), outline_color=None, outline_thickness=2):
        """Render text with optional outline (stroke) effect."""
        base = self.font.render(text, True, text_color)

        if outline_color:
            outline = pygame.Surface(
                (base.get_width() + 2 * outline_thickness, base.get_height() + 2 * outline_thickness),
                pygame.SRCALPHA
            )

            for dx in range(-outline_thickness, outline_thickness + 1):
                for dy in range(-outline_thickness, outline_thickness + 1):
                    if dx != 0 or dy != 0:
                        outline.blit(
                            self.font.render(text, True, outline_color),
                            (dx + outline_thickness, dy + outline_thickness)
                        )

            outline.blit(base, (outline_thickness, outline_thickness))
            return outline
        else:
            return base
