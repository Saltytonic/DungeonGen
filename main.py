import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import numpy as np

class Game:
    """Game object for managing everything"""
    def __init__(self):
        pygame.init()
        self.running = False
        self.event_handler = EventHandler(self)
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.rng = np.random.default_rng()
        self.dungeon = Dungeon()

    def create_window(self, name, icon_path, width, height):
        self.window = pygame.display.set_mode((width, height))
        self.icon = pygame.image.load(icon_path)
        pygame.display.set_caption(name)
        pygame.display.set_icon(self.icon)

    def start(self):
        self.running = True

        while self.running is True:
            self.event_handler.get_events()
            self.event_handler.handle_events()

            self.window.fill((255, 255, 255))

            if not self.dungeon.is_generated():
                self.dungeon.create(1)

            if self.dungeon.is_generated():
                self.dungeon.draw(self.window)

            self.draw_coords()

            pygame.display.update()

    def create_dungeon(self):
        self.dungeon.create(1)

    def clear_dungeon(self):
        self.dungeon.clear()

    def stop(self):
        self.running = False

    def create_text(self, input_text):
        """Returns a text surface and rect for each text object to create."""
        text_surface = font.render(input_text, True, (0, 0, 0))
        return text_surface, text_surface.get_rect()

    def draw_coords(self):
        """Draws coordinates at each grid on the screen."""
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        mouse_coords = str("%s, %s" % (str(mouse_x), str(mouse_y)))
        text_surf, text_rect = self.create_text(mouse_coords)
        text_rect.center = (50, 20)
        self.window.blit(text_surf, text_rect)

class Dungeon:
    """Holds objects that define the dungeon"""
    def __init__(self):
        self.generated = False
        self.rooms = []
        self.halls = []

    def clear(self):
        """Empties the dungeon without saving"""
        self.rooms = []
        self.halls = []
        self.generated = False
        print("Poof! The dungeon is gone.")

    def create(self, room_qty):
        print("I would have generated a dungeon here...")
        self.generated = True

    def draw(self, surface):
        pass

    def is_generated(self):
        return self.generated

class EventHandler:
    """Handles events"""
    def __init__(self, Game):
        self.events = []
        self.game = Game

    def get_events(self):
        self.events = pygame.event.get()

    def handle_events(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.game.clear_dungeon()
                else:
                    self.game.clear_dungeon()
                    self.game.create_dungeon()

DungeonGen = Game()
DungeonGen.create_window("DungeonGen", "media/door.png", 800, 600)
DungeonGen.start()
