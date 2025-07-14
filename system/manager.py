class SceneManager:
    def __init__(self):
        self.current_scene = None

    def switch_to(self, scene):
        if self.current_scene:
            self.current_scene.exit()
        self.current_scene = scene
        self.current_scene.enter()

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)
