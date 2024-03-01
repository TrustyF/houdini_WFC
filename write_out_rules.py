import hou
import numpy as np
import json

node = hou.pwd()
geo = node.geometry()

processed = []
output = []


for point in geo.points():
    id = point.attribValue("piece")
    hashes = point.attribValue("side_hash")

    if id in processed:
        continue

    output.append(
        {
            "piece": id,
            "side_hash": {
                "z+": (hashes[1]),
                "z-": (hashes[3]),
                "x+": (hashes[0]),
                "x-": (hashes[2]),
            },
        }
    )

    processed.append(id)

with open("$HIP/JSON/rules.json", "w") as json_file:
    json.dump(output, json_file, indent=2)
