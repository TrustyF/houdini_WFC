import hou
import numpy as np
import json

node = hou.pwd()
geo = node.geometry()

processed = []
output = []


def main():
    for point in geo.points():
        id = point.attribValue("piece")
        hashes = point.attribValue("side_hash")

        if id in processed:
            continue

        output.append({"piece": id, "side_hash": hashes})

        processed.append(id)

    with open(
        "C:\\A_Mod\\A_Projects\\Houdini\\Backrooms_WFC\\JSON\\rules.json", "w"
    ) as json_file:
        json.dump(output, json_file, indent=2)
