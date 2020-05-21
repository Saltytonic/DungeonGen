import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
#from itertools import chain
import random
import math
from dataclasses import dataclass

# Initialization
pygame.init()
random.seed()

# Title and Icon
pygame.display.set_caption("DungeonGen")
icon = pygame.image.load("media/door.png")
pygame.display.set_icon(icon)

# Global values
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
ROOM_SIZE = 10

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

@dataclass
class TileType:
    """Struct-like object for holding tile type"""
    type: int = -1
    empty: int = -1
    invalid: int = 0
    room: int = 1

# Creates a list of tuples representing each point with coordinate data
# The third element in the tuple will hold an identifier for the tile type
MAP_X = int(WIDTH/GRID_SIZE)
MAP_Y = int(HEIGHT/GRID_SIZE)

def clamp(n, minn, maxn):
    out1 = min(maxn, n)
    return max(out1, minn)

def build_room(room_pos, grid):
    """Takes the room center pos and removes all invalid locations around it in order to "build"
    the room. Stores new tiles in output."""
    #print("Room choice was ", room_pos)

    half = math.floor(ROOM_SIZE/2)

    for _x in range(ROOM_SIZE):
        for _y in range(ROOM_SIZE):
            _x1 = clamp(room_pos[0]-_x, 0, MAP_X-1)
            _x2 = clamp(room_pos[0]+_x, 0, MAP_X-1)
            _y1 = clamp(room_pos[1]-_y, 0, MAP_Y-1)
            _y2 = clamp(room_pos[1]+_y, 0, MAP_Y-1)

            if _x > half or _y > half:
                set_state = TileType.invalid
            else:
                set_state = TileType.room

            if grid[_x1][_y1][2].type == TileType.empty or set_state == TileType.room:
                grid[_x1][_y1][2].type = set_state

            if grid[_x1][_y2][2].type == TileType.empty or set_state == TileType.room:
                grid[_x1][_y2][2].type = set_state

            if grid[_x2][_y1][2].type == TileType.empty or set_state == TileType.room:
                grid[_x2][_y1][2].type = set_state

            if grid[_x2][_y2][2].type == TileType.empty or set_state == TileType.room:
                grid[_x2][_y2][2].type = set_state

def build_grid():
    """Returns an empty grid equal in size to the screen size."""
    empty_grid = [[(x, y, TileType()) for y in range(MAP_Y)] for x in range(MAP_X)]
    return empty_grid

def generate_map(num_of_rooms, grid):
    """ Returns an array of coordinates where each room should be."""
    for _ in range(num_of_rooms):
        choice = random.choice(get_valid_grid(grid))
        build_room(choice, grid)

def text_objects(input_text, font):
    """Returns a text surface and rect for each text object to create."""
    text_surface = font.render(input_text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()

def mark_border_invalid(grid):
    """Marks all tiles within floor(room_size/2)+1 as invalid for \
        room building purposes."""
    # Distance to not spawn rooms in
    edge_buffer = math.floor(ROOM_SIZE/2) + 1
    #print("Cols: ", len(grid))
    #print("Rows: ", len(grid[0]))
    #print("---------------------------")
    for _x_pos, _col in enumerate(grid):
        for _y_pos, _row in enumerate(grid[_x_pos]):
            if (_x_pos < edge_buffer) or (_x_pos >= (len(grid)-edge_buffer)) or \
                (_y_pos < edge_buffer) or (_y_pos >= (len(grid[_x_pos])-edge_buffer)):
                #print("Accessing [", _x_pos, ", ", _y_pos, "] ... ")
                grid[_x_pos][_y_pos][2].type = TileType.invalid

def get_valid_grid(grid_list):
    """
    Returns a copy of the 2D coordinate array with invalid positions \
        removed as a 1D array of tuples.
    """
    # grid_list is the 2D coord array, each row is a list of tuples, col is a tuple
    copy = [j for i in grid_list for j in i if j[2].type == TileType.empty]

    return copy

def get_rooms(grid_list):
    """
    Returns a copy of the 2D coordinate array with room positions as \
        a 1D array of coordinate tuples.
    """
    # grid_list is the 2D coord array, each row is a list of tuples, col is a
    # tuple
    copy = [j for i in grid_list for j in i if j[2].type == TileType.room]

    return copy

def get_border(grid_list):
    """
    Returns a copy of the 2D coordinate array with room positions as \
        a 1D array of coordinate tuples.
    """
    # grid_list is the 2D coord array, each row is a list of tuples, col is a
    # tuple
    copy = [j for i in grid_list for j in i if j[2].type == TileType.invalid]

    return copy

# Game Loop
RUNNING = True
GENERATED = False
small_font = pygame.font.Font('freesansbold.ttf', 9)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            GENERATED = False

    screen.fill((255, 255, 255))

    # Add text coords to each tile in the grid
    for col in range(math.floor(WIDTH/GRID_SIZE)):
        for row in range(math.floor(HEIGHT/GRID_SIZE)):
            x_pos = col * GRID_SIZE
            y_pos = row * GRID_SIZE
            TEXT = str("%s,%s" % (str(x_pos), str(y_pos)))
            text_surf, text_rect = text_objects(TEXT, small_font)
            text_rect.center = ((GRID_SIZE/2) + x_pos, (GRID_SIZE/2) + y_pos)
            screen.blit(text_surf, text_rect)

    # Only run when new generation
    if not GENERATED:
        # Create a new empty grid
        map_grid = build_grid()

        # Mark all the borders as invalid (optional, but suggested)
        mark_border_invalid(map_grid)

        # Marks all rooms on the map_grid
        ROOM_COUNT = 5
        generate_map(ROOM_COUNT, map_grid)

        rooms = get_rooms(map_grid)
        invalids = get_border(map_grid)

        # Blocks generating a new room every update
        GENERATED = True

    for room in rooms:
        rect = pygame.Rect(room[0]*GRID_SIZE, room[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, (0, 0, 0), rect)

    for invalid in invalids:
        rect = pygame.Rect(invalid[0]*GRID_SIZE, invalid[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), rect)

    pygame.display.update()
