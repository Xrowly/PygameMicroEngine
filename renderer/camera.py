class Camera:
    def __init__(self, world_width, world_height, viewport_width, viewport_height, deadzone_width=100):
        self.world_width = world_width
        self.world_height = world_height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        # Deadzone defines horizontal area in center where player moves freely without camera moving
        self.deadzone_width = deadzone_width

        # Camera's top-left position in the world coords
        self.x = 0
        self.y = 0  # assuming no vertical scrolling; can add similar logic if needed

    def update(self, player_rect):
        # Center of player in world coords
        player_x = player_rect.centerx

        # Left and right bounds of the deadzone relative to camera viewport
        deadzone_left = self.x + (self.viewport_width - self.deadzone_width) // 2
        deadzone_right = deadzone_left + self.deadzone_width

        # Move camera left if player goes past deadzone right edge
        if player_x > deadzone_right:
            self.x = player_x - (self.viewport_width + self.deadzone_width) // 2

        # Move camera right if player goes past deadzone left edge
        elif player_x < deadzone_left:
            self.x = player_x - (self.viewport_width - self.deadzone_width) // 2

        # Clamp camera to world boundaries
        self.x = max(0, min(self.x, self.world_width - self.viewport_width))
        self.y = 0  # add vertical clamping if you scroll vertically

    def apply(self, target_rect):
        # Return the rectangle shifted by camera offset to draw on screen
        return target_rect.move(-self.x, -self.y)
