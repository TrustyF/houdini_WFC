import hou
import json
import random

node = hou.pwd()
geo = node.geometry()

# import rules
with open("C:\\A_Mod\\A_Projects\\Houdini\\Backrooms_WFC\\JSON\\rules.json") as json_file:
    rules = json.load(json_file)

iteration = node.inputs()[1].geometry().attribValue("iteration")

rows = 2
cols = 10
grid = []

random.seed(0)

geo.addAttrib(hou.attribType.Point, "piece", -1)
geo.addAttrib(hou.attribType.Point, "possibilities", 0)
geo.addAttrib(hou.attribType.Point, "poss", "")
geo.addAttrib(hou.attribType.Point, "rotation", 0)


def decode_tile(tile):
    return int(tile.split("_")[0]), int(tile.split("_")[1])


def diff_array(original_array, filter_array):
    return [x for x in original_array if x in filter_array]


def define_grid():
    global grid
    possibilities = [f'{k}_{x}' for x in range(4) for k in range(len(rules))]
    grid = [[possibilities for i in range(cols)] for j in range(rows)]


def make_grid():
    for i in range(rows):
        for j in range(cols):
            point = geo.createPoint()
            point.setPosition((i, 0, j))
            point.setAttribValue("possibilities", len(grid[i][j]))
            point.setAttribValue("poss", str(grid[i][j]))

            if len(grid[i][j]) == 1:
                data = decode_tile(grid[i][j][0])
                point.setAttribValue("piece", data[0])
                point.setAttribValue("rotation", data[1])


def get_lowest_entropy():
    smallest = -1
    index = -1

    for i in range(rows):
        for j in range(cols):

            if len(grid[i][j]) <= 1:
                continue

            if len(grid[i][j]) < smallest or smallest == -1:
                smallest = len(grid[i][j])
                index = (i, j)

    return index


def propagate(index):
    print("propagating", index)
    x, y = index
    piece = decode_tile(grid[x][y][0])[0]

    # look ahead
    ahead = y + 1
    if ahead < cols:
        grid[x][ahead] = diff_array(grid[x][ahead], rules[piece]["side_piece"]["z-"])

    # look behind
    behind = y - 1
    if behind > -1:
        grid[x][behind] = diff_array(grid[x][behind], rules[piece]["side_piece"]["z+"])

    # look left
    left = x - 1
    if left > -1:
        grid[left][y] = diff_array(grid[left][y], rules[piece]["side_piece"]["x-"])

    # look right
    right = x + 1
    if right < rows:
        grid[right][y] = diff_array(grid[right][y], rules[piece]["side_piece"]["x+"])


def collapse(index):
    x, y = index
    possibilities = len(grid[x][y])
    grid[x][y] = [grid[x][y][random.randint(0, possibilities - 1)]]


def main():
    define_grid()

    for i in range(iteration):
        low = get_lowest_entropy()
        collapse(low)
        propagate(low)

    make_grid()
