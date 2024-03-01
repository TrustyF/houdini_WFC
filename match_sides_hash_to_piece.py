import hou
import json

node = hou.pwd()
geo = node.geometry()


def main():
    with open(
        "C:\\A_Mod\\A_Projects\\Houdini\\Backrooms_WFC\\JSON\\rules.json"
    ) as json_file:
        rules = json.load(json_file)

    for piece in rules:

        matched = {"x+": [], "z-": [], "z+": [], "x-": []}

        for compare_piece in rules:

            if piece["piece"] == compare_piece["piece"]:
                continue

            for side, side_label in enumerate(["x+", "z+", "x-", "z-"]):

                for rot in range(4):

                    def wrap_i(i):
                        return i % 4

                    if (
                        piece["side_hash"][wrap_i(side)]
                        == compare_piece["side_hash"][wrap_i(side + rot + 2)]
                    ):
                        matched[side_label].append(f'{compare_piece["piece"]}_{rot}')

        piece["side_piece"] = matched

    with open(
        "C:\\A_Mod\\A_Projects\\Houdini\\Backrooms_WFC\\JSON\\rules.json", "w"
    ) as json_file:
        json.dump(rules, json_file, indent=2)
