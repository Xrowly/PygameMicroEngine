import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, color, width, height, pos, text="", font_size=20,
                 text_color=(255, 255, 255, 255),
                 hover_color=None, click_color=None,
                 hover_text_color=None, click_text_color=None,
                 border_color=(0,0,0,0), hover_border_color=None, click_border_color=None,
                 border_width=0,
                 fancy_text=None,
                 click_callback=None):
        pygame.sprite.Sprite.__init__(self)

        # Colors
        self.normal_color = color
        self.hover_color = hover_color if hover_color is not None else self._brighten_color(color)
        self.click_color = click_color if click_color is not None else self._darken_color(color)
        self.current_color = self.normal_color

        # Border colors & width
        self.border_color = border_color
        self.hover_border_color = hover_border_color if hover_border_color is not None else self._brighten_color(border_color)
        self.click_border_color = click_border_color if click_border_color is not None else self._darken_color(border_color)
        self.current_border_color = self.border_color
        self.border_width = border_width

        # Position and size
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

        # Text
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, self.font_size)

        self.text_color_normal = text_color
        self.text_color_hover = hover_text_color if hover_text_color is not None else text_color
        self.text_color_click = click_text_color if click_text_color is not None else text_color
        self.current_text_color = self.text_color_normal

        # States
        self.is_hovered = False
        self.is_clicked = False

        # Fancy text renderer (optional)
        self.fancy_text = fancy_text

        # Callback
        self.click_callback = click_callback
        self._render_button()

    def _brighten_color(self, color, factor=0.2):
        return tuple(min(255, int(c + (255 - c) * factor)) for c in color[:3]) + ((color[3],) if len(color) == 4 else (255,))

    def _darken_color(self, color, factor=0.2):
        return tuple(max(0, int(c * (1 - factor))) for c in color[:3]) + ((color[3],) if len(color) == 4 else (255,))

    def _render_button(self):
        self.image.fill((0, 0, 0, 0))  # Clear transparent

        # Background fill if alpha > 0
        if len(self.current_color) == 4 and self.current_color[3] > 0:
            bg_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            bg_surf.fill(self.current_color)
            self.image.blit(bg_surf, (0, 0))
        elif len(self.current_color) == 3:
            self.image.fill(self.current_color)

        # Draw border if visible
        if self.border_width > 0:
            alpha = self.current_border_color[3] if len(self.current_border_color) == 4 else 255
            if alpha > 0:
                border_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                pygame.draw.rect(border_surf, self.current_border_color, border_surf.get_rect(), self.border_width)
                self.image.blit(border_surf, (0, 0))

        # Render text if visible
        if self.text:
            alpha = self.current_text_color[3] if len(self.current_text_color) == 4 else 255
            if alpha > 0:
                if self.fancy_text:
                    text_surf = self.fancy_text.render(self.text, self.current_text_color)
                else:
                    text_surf = self.font.render(self.text, True, self.current_text_color)
                text_rect = text_surf.get_rect(center=self.image.get_rect().center)

                # If fully transparent background, resize button to text size
                if self.normal_color == (0, 0, 0, 0):
                    self.image = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
                    self.rect = self.image.get_rect(center=self.rect.center)
                    self.image.blit(text_surf, (0, 0))
                else:
                    self.image.blit(text_surf, text_rect)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        was_clicked = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.is_clicked = True
                    self.current_color = self.click_color
                    self.current_text_color = self.text_color_click
                    self.current_border_color = self.click_border_color
                    self._render_button()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.rect.collidepoint(event.pos) and self.is_clicked:
                    was_clicked = True
                self.is_clicked = False

        is_hovering = self.rect.collidepoint(mouse_pos)
        if is_hovering != self.is_hovered or was_clicked:
            self.is_hovered = is_hovering
            if self.is_clicked:
                self.current_color = self.click_color
                self.current_text_color = self.text_color_click
                self.current_border_color = self.click_border_color
            elif self.is_hovered:
                self.current_color = self.hover_color
                self.current_text_color = self.text_color_hover
                self.current_border_color = self.hover_border_color
            else:
                self.current_color = self.normal_color
                self.current_text_color = self.text_color_normal
                self.current_border_color = self.border_color
            self._render_button()

        if was_clicked:
            self.handle_click()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_click(self):
        if self.click_callback:
            try:
                self.click_callback(self)  # Pass self if callback needs it
            except Exception as e:
                print(f"[ERROR] Button callback failed: {e}")
        else:
            print(f"Button '{self.text}' was clicked! (No callback)")
