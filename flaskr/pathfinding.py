class Tile():
    def __init__(self, x, y, type="empty", id=None):
        self.type = type
        self.id = id
        self.pos = {"x": x, "y": y}
        self.visited = False
    def isEmpty(self):
        return self.type == "empty"
    def isRoom(self):
        return self.type == "room"
    def isHallway(self):
        return self.type == "hall"
    def setType(self, type):
        self.type = type
"""
grid = [
            [
                #im cool for using the ternary tuple
                Tile()
                if not
                ((y == 0) or
                (y == 2 and (x in range(4) or x in range(5, 9))) or
                (y in range(3, 9) and (x in [3, 5])))
                else
                if
            for x in range(9)]
        for y in range(9)]
"""

map = [
    ["r", "r", "r", "r", "r", "r", "r", "r", "r"],
    ["h", "h", "h", "h", "h", "h", "h", "h", "h"],
    ["r", "r", "r", "r", "h", "r", "r", "r", "r"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
]

grid = [[Tile(x, y) if map[y][x] == "e" else Tile(x, y, "hall") if map[y][x] == "h" else Tile(x, y, "room", str(x) + str(y))
        for x in range(len(map[y]))] for y in range(len(map))]

def get_room_from_id(id, grid):
    for row in grid:
        for tile in row:
            if tile.type == "room" and tile.id == id:
                return tile

def get_tile(x, y, grid):
    for row in grid:
        for tile in row:
            if tile.pos["x"] == x and tile.pos["y"] == y:
                return tile
    return None #if it can't find the tile

def get_adjacent_tiles(x, y, grid):
    tiles = [tile for tile in [
        get_tile(x + 1, y, grid),
        get_tile(x - 1, y, grid),
        get_tile(x, y + 1, grid),
        get_tile(x, y - 1, grid)
    ] if tile != None]

    return tiles


def get_dist(start_id, end_id, grid):
    x = get_room_from_id(start_id, grid).pos["x"]
    y = get_room_from_id(start_id, grid).pos["y"]
    dist = 0
    branch_points = [] #these are in order of how far back the branch points are

    while True:
        dist += 1
        currentTile = get_tile(x, y, grid)
        currentTile.visited = True
        if len(branch_points) > 0: #i actually don't think this will be needed but maybe
            branch_points[-1]["visited_tiles"].append(currentTile)
        adj_hallways = []
        #scan the adjacent tiles
        for tile in get_adjacent_tiles(x, y, grid):
            #check if it got to the target room
            if tile.type == "room" and tile.id == end_id:
                    return dist
            elif tile.type == "hall" and not tile.visited:
                adj_hallways.append(tile) #TODO: make sure that previous hallways aren't included
        #decide what to do based on number of hallways
        if len(adj_hallways) == 1:
            #only one option, so let's go there
            x, y = adj_hallways[0].pos["x"], adj_hallways[0].pos["y"]
            continue #go to top of loop
        elif len(adj_hallways) > 1:
            #make a new branch point record if we dont have one already
            #visited tiles are the tiles after that branch point but before the next
            #im using them so that if we go back to the branch point, we can unvisit the tiles
            if not any(d["coords"] == (x, y) for d in branch_points):
                branch_points.append({"coords": (x, y), "adj_hallways": adj_hallways,
                "visited_tiles": [], "dist_to_start": dist})
            #go to one of the adjacent hallways and delete it from the list
            for bp in branch_points:
                if bp["coords"] == (x, y):
                    new_pos = bp["adj_hallways"].pop(0).pos
                    x, y = new_pos["x"], new_pos["y"]
                    #if there are no more adj hallways, remove the branch point
                    #and go back to previous branch point
                    #it should never revisit a branch point thats been removed
                    #but if im wrong and it does this will 100% break the algorithm
                    if len(bp["adj_hallways"]) == 0:
                        for vt in bp["visited_tiles"]: #this should honestly never be needed
                            vt.visited = False
                        dist = bp["dist_to_start"]
                        branch_points.remove(bp)
                        x, y = branch_points[-1]["coords"][0], branch_points[-1]["coords"][1]
                    continue
            continue
        elif len(adj_hallways) < 1:
            #nowhere left to go
            #just go back to the last recorded branch point (which should be the last one visited)
            dist = branch_points[-1]["dist_to_start"] #reset distance
            x, y = branch_points[-1]["coords"][0], branch_points[-1]["coords"][1]
            continue


def disp_grid(grid):
    for row in grid:
        print [tile.id for tile in row]

disp_grid(grid)

print get_dist("00", "70", grid)
