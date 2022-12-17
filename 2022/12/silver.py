import numpy as np

import tools.graph.dijkstra

height = None
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        line = np.array([_ for _ in line])
        if height is None:
            height = line
        else:
            height = np.vstack([height, line])

start = np.nonzero(height == 'S')
start = tuple(zip(*start))[0]
end = np.nonzero(height == 'E')
end = tuple(zip(*end))[0]
height[start] = 'a'
height[end] = 'z'


def map_letter_to_height(l: str) -> int:
    if l == 'S':
        l = 'a'
    elif l == 'E':
        l = 'z'
    return ord(l) - ord('a')


height = np.vectorize(map_letter_to_height)(height)
print(height)

edge_cost: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
it = np.nditer(height, flags=['multi_index'])
for current_height in it:
    current_loc = it.multi_index
    can_go: list[tuple[int, int]] = []
    if current_loc[0] > 0:  # can go left
        can_go.append((current_loc[0] - 1, current_loc[1]))
    if current_loc[0] < height.shape[0]-1:  # can go right
        can_go.append((current_loc[0] + 1, current_loc[1]))
    if current_loc[1] > 0:  # can go up
        can_go.append((current_loc[0], current_loc[1] - 1))
    if current_loc[1] < height.shape[1]-1:  # can go down
        can_go.append((current_loc[0], current_loc[1] + 1))
    for next_loc in can_go:
        if height[next_loc] <= current_height + 1:
            edge_cost[current_loc, next_loc] = 1

d = tools.graph.dijkstra.dijkstra(
    edge_costs=edge_cost,
    node_to_calculate_to=end,
)
print(d[start])
