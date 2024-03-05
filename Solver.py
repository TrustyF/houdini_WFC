import hou
import json
import random

node = hou.pwd()
geo = node.geometry()

# import rules
with open("C:\\A_Mod\\A_Projects\\Houdini\\Backrooms_WFC\\JSON\\rules.json") as json_file:
    rules = json.load(json_file)

rows = 10
cols = 10
grid = []

geo.addAttrib(hou.attribType.Point, "piece", -1)
geo.addAttrib(hou.attribType.Point, "rotation", 0)


def define_grid():
    global grid
    possibilities = [f'{k}_{x}' for x in range(4) for k in range(len(rules))]
    grid = [[possibilities for i in range(cols)] for j in range(rows)]


def make_grid():
    for i in range(rows):
        for j in range(cols):
            point = geo.createPoint()
            point.setPosition((i, 0, j))

            if len(grid[i][j]) < 2:
                point.setAttribValue("piece", int(grid[i][j][0].split("_")[0]))
                point.setAttribValue("rotation", int(grid[i][j][0].split("_")[1]))


def get_random_piece():
    return str(rules[random.randint(0, len(rules) - 1)]["piece"]) + "_0"


def get_lowest_entropy():
    smallest = -1
    index = -1

    for i in range(rows):
        for j in range(cols):
            if len(grid[i][j]) < smallest or smallest == -1:
                smallest = len(grid[i][j])
                index = (i, j)

    return index


def propagate(index):
    x, y = index
    # look top
    if y <= cols:




def main():
    define_grid()
    grid[1][2] = [get_random_piece()]

    for i in range(10):
        propagate(get_lowest_entropy())

    make_grid()
