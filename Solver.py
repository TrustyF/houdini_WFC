import hou
import json
import random

node = hou.pwd()
geo = node.geometry()

rules = []
# import rules
with open("$HIP/JSON/rules.json") as json_file:
    rules = json.load(json_file)

total_points = len(geo.iterPoints())
iter = node.inputs()[1].geometry().attribValue("iteration")


def get_random_piece():
    return rules[random.randint(0, len(rules) - 1)]["piece"]


def solve(i):
    # print("solve", i)

    piece = geo.point(i).attribValue("piece")
    ptnum = i

    if piece == -1:
        return False

    def solve_front():
        if ptnum + 1 >= total_points:
            return False

        front_pt = geo.point(ptnum + 1).attribValue("piece")

        if front_pt == -1:
            if len(rules[piece]["side_piece"]["x+"]) > 0:
                picked_piece = random.choice(rules[piece]["side_piece"]["x+"])
                geo.point(ptnum + 1).setAttribValue("piece", picked_piece)

    def solve_back():
        if ptnum - 1 < 0:
            return False

        back_pt = geo.point(ptnum - 1).attribValue("piece")

        if back_pt == -1:
            if len(rules[piece]["side_piece"]["x-"]) > 0:
                picked_piece = random.choice(rules[piece]["side_piece"]["x-"])
                geo.point(ptnum - 1).setAttribValue("piece", picked_piece)

    def solve_left():
        if ptnum - 10 < 0:
            return False

        left_pt = geo.point(ptnum - 10).attribValue("piece")

        if left_pt == -1:
            if len(rules[piece]["side_piece"]["z-"]) > 0:
                picked_piece = random.choice(rules[piece]["side_piece"]["z-"])
                geo.point(ptnum - 10).setAttribValue("piece", picked_piece)

    def solve_right():

        if ptnum + 10 >= total_points:
            return False

        right_pt = geo.point(ptnum + 10).attribValue("piece")

        if right_pt == -1:
            if len(rules[piece]["side_piece"]["z+"]) > 0:
                picked_piece = random.choice(rules[piece]["side_piece"]["z+"])
                geo.point(ptnum + 10).setAttribValue("piece", picked_piece)

    solve_front()
    solve_back()
    solve_left()
    solve_right()

    return True


for i in range(iter):
    for point in geo.points():
        if solve(point.number()):
            break
    # solve(i)
