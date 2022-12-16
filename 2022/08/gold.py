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

it = np.nditer(forest, flags=['multi_index'])
scenic_score = np.empty(forest.shape)
for tree in it:
    visible_left = 0
    for x in range(it.multi_index[1]-1, -1, -1):
        visible_left += 1
        if forest[it.multi_index[0], x] >= tree:
            break

    visible_right = 0
    for x in range(it.multi_index[1]+1, forest.shape[1], 1):
        visible_right += 1
        if forest[it.multi_index[0], x] >= tree:
            break

    visible_top = 0
    for y in range(it.multi_index[0]-1, -1, -1):
        visible_top += 1
        if forest[y, it.multi_index[1]] >= tree:
            break

    visible_bottom = 0
    for y in range(it.multi_index[0]+1, forest.shape[0], 1):
        visible_bottom += 1
        if forest[y, it.multi_index[1]] >= tree:
            break

    scenic_score[it.multi_index] = visible_left * visible_right * visible_bottom * visible_top

print(scenic_score)
print(np.max(scenic_score))

