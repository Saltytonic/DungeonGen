from itertools import chain
import helperfuncs as hf
import random
import math
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

# Initialization

pygame.init()
random.seed()

# Title and Icon
pygame.display.set_caption("DungeonGen")
icon = pygame.image.load("door3.png")
pygame.display.set_icon(icon)

# Global values
HEIGHT = 800
WIDTH = 600
GRID_SIZE = 20
ROOM_SIZE = 5

# Create the display
screen = pygame.display.set_mode((HEIGHT, WIDTH))

# Creates a list of tuples representing each point with coordinate data
# The third element in the tuple will hold an identifier for the tile type
mapX = int(WIDTH/GRID_SIZE)
mapY = int(HEIGHT/GRID_SIZE)
mapGrid = [[(x,y,-1) for x in range(mapY)] for y in range(mapX)]

# Distance to not spawn rooms in
edgeBuffer = math.floor(ROOM_SIZE/2) + 1

# Mark borders as invalid spots
for row in range(len(mapGrid)):
    for col in range(len(mapGrid[row])):
        if row <  edgeBuffer or row > len(mapGrid) or \
            col <  edgeBuffer or col > len(mapGrid[row]):
                temp = mapGrid[row][col]
                mapGrid[row][col] = (temp[0], temp[1], 0)

# Used for randomly selecting valid areas in destructive manner
validGrid = hf.validGrid(ROOM_SIZE, mapGrid)

numRooms = 3



# Game Loop
running = True
has_gen = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_gen = False

    screen.fill((255, 255, 255))

    if not has_gen:
        # Create the rooms on the mapGrid
        for i in range(numRooms):
            # Choose a spot for the room
            choice = random.choice(validGrid)
            mapGrid[choice[1]][choice[0]] = (choice[1], choice[0], 1)

        cur_state = list(chain.from_iterable(zip(*mapGrid)))
        has_gen = True

    for item in cur_state:
        # print(item[0], item[1])
        if item[2] == 1:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(item[1]*GRID_SIZE, item[0]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.update()