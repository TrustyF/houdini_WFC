import hou
import json
import random

node = hou.pwd()
geo = node.geometry()

rules = []
# import rules
with open(
    "C:\\A_Mod\\A_Projects\\Houdini\\Backrooms_WFC\\JSON\\rules.json"
) as json_file:
    rules = json.load(json_file)

total_points = len(geo.iterPoints())
iter = node.inputs()[1].geometry().attribValue("iteration")

lowest_enthropy = 100


def get_random_piece():
    return rules[random.randint(0, len(rules) - 1)]["piece"]


def solve(i):
    global lowest_enthropy

    def collapse(ptnum):
        poss = possibility[random.randint(0, len(possibility) - 1)]
        geo.point(i).setAttribValue("piece", int(poss.split("_")[0]))
        geo.point(i).setAttribValue("rotations", int(poss.split("_")[1]))
        geo.point(i).setAttribValue("possibility", [])

    piece = geo.point(i).attribValue("piece")
    possibility = geo.point(i).attribValue("possibility")

    # skip if entropy is too high
    if len(possibility) > lowest_enthropy:
        return

    # collapse if possibility is 1
    if len(possibility) <= 2 and len(possibility) > 0 and piece == -1:
        collapse(i)
        return

    mapping = [[i + 1, "z+"], [i - 1, "z-"], [i - 10, "x+"], [i + 10, "x-"]]

    for side_cell in mapping:

        # skip out of bounds
        if side_cell[0] < 0 or side_cell[0] > total_points - 1:
            continue

        # print(side_cell[0])

        # prep attributes
        side_piece = geo.point(side_cell[0]).attribValue("piece")

        # skip if solved
        if side_piece != -1:
            continue

        current_poss = geo.point(side_cell[0]).attribValue("possibility")
        rule_poss = rules[piece]["side_piece"][side_cell[1]]
        result_list = [x for x in current_poss if x in rule_poss]
        geo.point(side_cell[0]).setAttribValue("possibility", result_list)
        lowest_enthropy = len(result_list)


def main():
    global lowest_enthropy

    for point in geo.points():
        num_poss = len(point.attribValue("possibility"))
        if num_poss < lowest_enthropy:
            lowest_enthropy = num_poss

    for i in range(iter):
        for point in geo.points():
            solve(point.number())
        # solve(i)
