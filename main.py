# Imports
from itertools import chain
import helperfuncs as hf
import pygame
import random

# Initialization
pygame.init()
random.seed()

# Title and Icon
pygame.display.set_caption("DungeonGen")
icon = pygame.image.load("door3.png")
pygame.display.set_icon(icon)

# Global values
HEIGHT = 100
WIDTH = 100
GRID_SIZE = 10
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
for row in mapGrid:
    for col in mapGrid[row]:
        if row < 

# Used for randomly selecting valid areas in destructive manner
validGrid = hf.edgelessValidGrid(ROOM_SIZE, mapGrid)

# Create the rooms on the mapGrid
for i in range(numRooms):
    # Choose a spot for the room
    choice = random.choice(validGrid)

    # Update the mapGrid to 


# Game Loop
running = True
has_gen = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_gen = False

    screen.fill((137, 137, 137))

    if not has_gen:
        cur_state = gen_state()
        has_gen = True
    
    for item in cur_state:
        pygame.draw.rect(screen, item[0], item[1])


    pygame.display.update()