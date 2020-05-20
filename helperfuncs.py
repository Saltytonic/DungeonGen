import math

def edgelessValidGrid(ROOM_SIZE, gridList):
    # Remove edges and combine into one huge list
    copy = [i[edgeBuffer:-edgeBuffer] for i in gridList[edgeBuffer:-edgeBuffer]]
    copy = list(chain.from_iterable(zip(*copy)))
    
    return copy