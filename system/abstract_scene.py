from abc import ABC, abstractmethod

class AbstractScene(ABC):
    @abstractmethod
    def enter(self): pass

    @abstractmethod
    def exit(self): pass

    @abstractmethod
    def handle_events(self, events): pass

    @abstractmethod
    def update(self, dt): pass

    @abstractmethod
    def draw(self, screen): pass
