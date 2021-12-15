"""
Note: not optimal. Took way to long to calculate. Needs optimisation.
Ideas: prune bad paths?
"""

import numpy

from tools import dijkstra

grid = None
with open("15.input.txt", "r") as f:
    for line in f.readlines():
        numbers = [int(_) for _ in list(line.strip())]
        if grid is None:
            grid = [numbers]
        else:
            grid = numpy.concatenate((grid, [numbers]), axis=0)

grid = numpy.swapaxes(grid, 0, 1)  # make grid[x, y]

print(grid.transpose())  # transpose to show Y vertically

# now extend the grid
grid = numpy.concatenate([grid, grid+1, grid+2, grid+3, grid+4], axis=0)
grid = numpy.concatenate([grid, grid+1, grid+2, grid+3, grid+4], axis=1)
grid = ((grid-1) % 9) + 1  # wrap 1->1, ..., 9->9, 10->1, 11->2, ...
print(grid.transpose())  # transpose to show Y vertically

edges = {}
with numpy.nditer(grid, flags=['multi_index']) as it:
    for value in it:
        x, y = it.multi_index
        # this node has (up to) 4 incoming edges
        if x > 0:  # from left
            edges[((x-1, y), (x, y))] = int(value)
        if x < grid.shape[0]-1:  # from right
            edges[((x+1, y), (x, y))] = int(value)
        if y > 0:  # from top
            edges[((x, y-1), (x, y))] = int(value)
        if y < grid.shape[1]-1:  # from bottom
            edges[((x, y+1), (x, y))] = int(value)

dest = (grid.shape[0] - 1, grid.shape[1] - 1)
costs = dijkstra.dijkstra(edges, dest)
# print(costs)
# p = (0, 0)
# while p != dest:
#     print(f'Moving from {p} to {costs[p].next_hop}')
#     p = costs[p].next_hop
print(costs[(0, 0)].cost)
