"""Loop principal e troca de cenas."""
import pygame
from . import config as C
from .fx import SoundBank, Vintage


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
        pygame.display.set_caption('KUNG-FOLK — folclore brasileiro')
        self.clock = pygame.time.Clock()
        self.sounds = SoundBank()
        self.vintage = Vintage()
        self.running = True
        from . import sprites
        from .characters import CHARACTERS
        sprites.load_all(CHARACTERS)          # usa sprites onde houver PNGs
        from .scenes import TitleScene
        self.scene = TitleScene(self)

    def switch(self, scene):
        self.scene = scene

    def step(self, events):
        pressed = {e.key for e in events if e.type == pygame.KEYDOWN}
        keys = pygame.key.get_pressed()
        self.scene.update(pressed, keys)
        self.scene.draw(self.screen)
        self.vintage.apply(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
            self.step(events)
            self.clock.tick(C.FPS)
        pygame.quit()
