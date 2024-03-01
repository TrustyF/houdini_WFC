import hou
import json

node = hou.pwd()
geo = node.geometry()

with open("$HIP/JSON/rules.json") as json_file:
    rules = json.load(json_file)

for piece in rules:

    matched = {"x+": [], "z-": [], "z+": [], "x-": []}

    for compare_piece in rules:

        if piece["piece"] == compare_piece["piece"]:
            continue

        if piece["side_hash"]["x+"] == compare_piece["side_hash"]["x-"]:
            matched["x+"].append(compare_piece["piece"])

        if piece["side_hash"]["x-"] == compare_piece["side_hash"]["x+"]:
            matched["x-"].append(compare_piece["piece"])

        if piece["side_hash"]["z+"] == compare_piece["side_hash"]["z-"]:
            matched["z+"].append(compare_piece["piece"])

        if piece["side_hash"]["z-"] == compare_piece["side_hash"]["z+"]:
            matched["z-"].append(compare_piece["piece"])

    piece["side_piece"] = matched


with open("$HIP/JSON/rules.json", "w") as json_file:
    json.dump(rules, json_file, indent=2)
