import math, time

class Tile():
    def __init__(self, x, y, level, type="empty", id=None):
        self.type = type
        self.id = id
        self.pos = {"x": x, "y": y}
        self.visited = False
        self.level = level
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
[
    ["r", "r", "r", "r", "r", "s2", "r", "r", "r"],
    ["h", "h", "h", "h", "h", "h", "h", "h", "h"],
    ["r", "r", "r", "r", "h", "r", "r", "r", "r"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "s1", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
],
[
    ["e", "e", "e", "r", "h", "s2", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["e", "e", "e", "r", "h", "r", "e", "e", "e"],
    ["r", "r", "r", "s1", "h", "r", "r", "r", "r"],
    ["h", "h", "h", "h", "h", "h", "h", "h", "h"],
    ["r", "r", "r", "r", "r", "r", "r", "r", "r"],
]]


DIST_PER_FLOOR = 2

grid = [
    [
        [Tile(x, y, z) if map[z][y][x] == "e"
        else (Tile(x, y, z, "hall") if map[z][y][x] == "h"
        else Tile(x, y, z, "room", str(z) + str(x) + str(y)) if map[z][y][x] == "r"
        else Tile(x, y, z, "stair", str(z) + map[z][y][x][-1]))
        for x in range(len(map[z][y]))]
    for y in range(len(map[z]))]
for z in range(len(map))]

def get_tile_from_id(id, grid):
    for level in grid:
        for row in level:
            for tile in row:
                if (tile.type == "room" or tile.type == "stair") and tile.id == id:
                    return tile

def get_tile(x, y, z, grid):
    for level in grid:
        for row in level:
            for tile in row:
                if tile.pos["x"] == x and tile.pos["y"] == y and tile.level == z:
                    return tile
    return None #if it can't find the tile

def get_adjacent_tiles(x, y, z, grid):
    tiles = [tile for tile in [
        get_tile(x + 1, y, z, grid),
        get_tile(x - 1, y, z, grid),
        get_tile(x, y + 1, z, grid),
        get_tile(x, y - 1, z, grid)
    ] if tile != None]

    return tiles

def get_staircases_on_level(z, grid):
    stairs = []
    for level in grid:
        for row in level:
            for tile in row:
                if tile.level == z and tile.type == "stair":
                    stairs.append(tile)

    return stairs




def get_dist_3d(start_id, end_id, grid):
    x = get_tile_from_id(start_id, grid).pos["x"]
    y = get_tile_from_id(start_id, grid).pos["y"]
    z1 = get_tile_from_id(start_id, grid).level
    z2 = get_tile_from_id(end_id, grid).level
    total_dist = 0
    #if they're on the same level we can just use the 2d dist function
    if get_tile_from_id(start_id, grid).level == get_tile_from_id(end_id, grid).level:
        return get_dist_2d(start_id, end_id, grid)
    else: #but if they're not, lets go to staircases
        #first we get the distances to all staircases on the level
        #print [get_dist_2d(start_id, stair.id, grid) for stair in get_staircases_on_level(z1, grid)]
        stair_dists = [(stair.id, get_dist_2d(start_id, stair.id, grid)) for stair in get_staircases_on_level(z1, grid)]
        #then we get the id of the closest staircase
        least_dist = 1000000
        least_dist_id = ""
        for sd in stair_dists:
            if sd[1] < least_dist:
                least_dist = sd[1]
                least_dist_id = sd[0]
        total_dist += least_dist
        #find the difference in floors
        total_dist += abs(z2 - z1) * DIST_PER_FLOOR
        #add distance from staircase on other floor to destination
        other_stair_id = str(z2) + least_dist_id[-1] #make id of other stair from level and staircase id
        total_dist += get_dist_2d(other_stair_id, end_id, grid)
        return total_dist


def get_dist_2d(start_id, end_id, grid):
    for level in grid:
        for row in level:
            for tile in row:
                tile.visited = False
    x = get_tile_from_id(start_id, grid).pos["x"]
    y = get_tile_from_id(start_id, grid).pos["y"]
    z = get_tile_from_id(start_id, grid).level
    dist = 0
    branch_points = [] #these are in order of how far back the branch points are

    while True:
        dist += 1
        currentTile = get_tile(x, y, z, grid)
        currentTile.visited = True
        if len(branch_points) > 0: #i actually don't think this will be needed but maybe
            branch_points[-1]["visited_tiles"].append(currentTile)
        adj_hallways = []
        #scan the adjacent tiles
        for tile in get_adjacent_tiles(x, y, z, grid):
            #check if it got to the target room
            if (tile.type == "room" or tile.type == "stair") and tile.id == end_id:
                    return dist
            elif tile.type == "hall" and not tile.visited:
                adj_hallways.append(tile)
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
                        branch_points.remove(bp)
                        for vt in bp["visited_tiles"]: #this should honestly never be needed
                            vt.visited = False
                        dist = bp["dist_to_start"]
                        x, y = branch_points[-1]["coords"][0], branch_points[-1]["coords"][1]
                    continue
            continue
        elif len(adj_hallways) < 1:
            #nowhere left to go
            #just go back to the last recorded branch point (which should be the last one visited)
            dist = branch_points[-1]["dist_to_start"] #reset distance
            x, y = branch_points[-1]["coords"][0], branch_points[-1]["coords"][1]
            if len(branch_points[-1]["adj_hallways"]) == 1:
                branch_points.remove(branch_points[-1]) #idk why but this works
            continue


def disp_grid(grid):
    for level in grid:
        print("-" * 60)
        for row in level:
            print([tile.id for tile in row])
    print("-" * 60)

disp_grid(grid)

roomIds = []
for level in grid:
    for row in level:
        for tile in row:
            if tile.type == "room":
                roomIds.append(tile.id)

def heres_a_distance_table_for_you_jeff():
    distance_lookup_table = {}
    for id in roomIds:
        distance_lookup_table[id] = {}
        for id2 in roomIds:
            distance_lookup_table[id][id2] = get_dist_3d(id, id2, grid)
            print(id, id2)
    return distance_lookup_table
