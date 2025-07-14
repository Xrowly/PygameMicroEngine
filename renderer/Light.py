import pygame; import math
#spotlights
class SpotLight:
    """
    Represents a SpotLight effect beam using elliptical gradient rendering.
    """

    def __init__(self, *, angle: float = None, beam_surface_size: tuple = None, display_surface: tuple=None):
        """
        Initialize the SpotLight effect with optional angle (in degrees) and beam size.

        Parameters:
        - angle (float): Beam angle in degrees. Default is 60° (π/3 radians).
        - beam_surface_size (tuple): Optional (width, height) for the beam's surface.
        """
        if display_surface is not None:
            self._screen = display_surface
        else:
            raise ValueError('display_surface cannot be None. Set display_surface as display_surface= (width,height)')
        self._width, self._height = self._screen
        self._beam_surface_size = beam_surface_size or (2 * self._width / 3, self._height / 2)
        self._angle_rad = math.pi / 3 if angle is None else angle * math.pi / 180

    @property
    def angle(self) -> float:
        """Get the current beam angle in radians."""
        return self._angle_rad

    @angle.setter
    def angle(self, degrees: float):
        """Set the beam angle in degrees (internally converted to radians)."""
        self._angle_rad = degrees * math.pi / 180

    @property
    def beam_surface_size(self) -> tuple:
        """Return the current beam surface size."""
        return self._beam_surface_size

    def _calculate_angle(self, pos, target) -> float:
        """Calculate angle between two vectors in degrees."""
        vector = target - pos
        angle_rad = math.atan2(vector.y, vector.x)
        return math.degrees(angle_rad)

    def _draw_ellipse_points(self, surface, color: tuple, angle: float):
        """
        Draw a polygonal approximation of an elliptical beam.
        Used to simulate light cones with transparency.
        """
        points = []
        x, y = self._beam_surface_size
        center = (0, y / 2)

        steps = 100
        start_angle = angle / 2
        end_angle = -angle / 2

        for i in range(steps + 1):
            t = i / steps
            theta = start_angle + t * (end_angle - start_angle)
            xx = center[0] + x * math.cos(theta)
            yy = center[1] + y * math.sin(theta)
            points.append((xx, yy))

        pygame.draw.polygon(surface, color, [center] + points)

    def create_beam(self, *, alpha: int = 90, steps: int = 90, debug: bool = False) -> pygame.Surface:
        """
        Create the SpotLight effect beam as a surface.

        Parameters:
        - alpha (int): Maximum transparency intensity (0–100)
        - steps (int): Number of fading layers
        - debug (bool): If True, fills beam with yellow for testing

        Returns:
        - pygame.Surface: The beam surface
        """
        if not isinstance(debug, bool):
            raise TypeError('debug must be a boolean')

        beam_surface = pygame.Surface(self._beam_surface_size, pygame.SRCALPHA)
        x, y=beam_surface.get_size()
        if debug:
            beam_surface.fill((255, 255, 0, 255))  # Debug yellow
            return beam_surface

        for i in range(steps):
            alpha_value = int((i / steps) * (alpha / 100) * 255)
            color = (0, 0, 0, alpha_value)
            self._draw_ellipse_points(beam_surface, color, self._angle_rad - (i / steps))
            
        return beam_surface

    def draw(self, surface: pygame.Surface, pos, target, rotation: float = 0):
        """
        Draw the SpotLight effect beam on a target surface, rotated to face a point.

        Parameters:
        - surface (pygame.Surface): The beam surface
        - pos (pygame.math.Vector2): Origin position of the SpotLight effect
        - target (pygame.math.Vector2): Target position to point the beam
        - rotation (float): Additional manual rotation angle

        Returns:
        - (rotated_image, rotated_rect): Beam image and its rect
        """
        center = surface.get_rect().center
        orbit_radius = self._width / 3
        angle_to_target = self._calculate_angle(pos, target)

        offset_x = orbit_radius * math.cos(math.radians(angle_to_target))
        offset_y = orbit_radius * math.sin(math.radians(angle_to_target))

        rotated_image = pygame.transform.rotate(surface, rotation - angle_to_target)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = (pos.x + offset_x, pos.y + offset_y)

        return rotated_image, rotated_rect

#circle_light_mask
def circle_light_mask(radius, steps, alpha):
    #making the mask
    light_mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    #updating the mask with Gradient
    for i in range(steps):
        alpha_value = int((i / steps) * (alpha / 100) * 255)
        color = (0, 0, 0, alpha_value)
        pygame.draw.circle(light_mask, color, (radius, radius), radius - (radius * i // steps))
    return light_mask
