import pygame

class FrameRateDisplay:
    def __init__(self, font_name="Arial", font_size=30, max_samples=10, color=(255, 255, 255), pos_fps=(10, 10), pos_time=(10, 40)):
        pygame.font.init()
        self.font = pygame.font.SysFont(font_name, font_size)
        self.color = color
        self.pos_fps = pos_fps
        self.pos_time = pos_time
        self.frame_times = []
        self.max_samples = max_samples

    def draw(self, surface, clock):
        fps = clock.get_fps() or 60  # fallback to 60 if zero
        elapsed_time = clock.get_time()

        self.frame_times.append(elapsed_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)

        avg_time = sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0
        rounded_time = self._round_to_nearest_even(avg_time)

        fps_text = self.font.render(f"FPS: {fps:.2f}", True, self.color)
        time_text = self.font.render(f"Frame Time: {rounded_time} ms", True, self.color)

        surface.blit(fps_text, self.pos_fps)
        surface.blit(time_text, self.pos_time)

    def _round_to_nearest_even(self, number):
        rounded = round(number)
        if rounded % 2 != 0:
            rounded -= 1 if rounded > number else -1
        return rounded
