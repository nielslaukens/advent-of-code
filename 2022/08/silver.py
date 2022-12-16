import numpy as np

forest = None
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        l = np.array([int(_) for _ in line])
        if forest is None:
            forest = l
        else:
            forest = np.vstack([
                forest,
                l
            ])

print(forest)


def f(line, reverse: bool = False):
    highest = -1
    visible = np.zeros(shape=line.shape)
    if reverse:
        line = np.flip(line)
    for i, tree in enumerate(line):
        if tree > highest:
            visible[i] = 1
            highest = tree
    if reverse:
        visible = np.flip(visible)
    return visible


visible_from_top = np.apply_along_axis(f, 0, forest)
visible_from_bottom = np.apply_along_axis(lambda l: f(l, True), 0, forest)
visible_from_left = np.apply_along_axis(f, 1, forest)
visible_from_right = np.apply_along_axis(lambda l: f(l, True), 1, forest)

visible = np.any([visible_from_top, visible_from_bottom, visible_from_left, visible_from_right], axis=0)
print(np.sum(visible))
