import pygame
from pygame.locals import *

class App:
    def __init__(self):
        self.running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()

    def draw_rect(self):
        pygame.draw.rect(self._display_surf, (0, 255, 0), (10, 10, 50, 50))


    def on_execute(self):
        if self.on_init() == False:
            self.running == False
        
        
        while (self.running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()



if __name__ == "__main__":
    app = App()
    app.on_execute()
    app.draw_rect()
    