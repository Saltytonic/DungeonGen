from itertools import chain
import math

def validGrid(ROOM_SIZE, gridList):
    # Remove edges and combine into one huge list
    copy = [col for row in gridList for col in row if col[2] != 0] 
    
    return copy