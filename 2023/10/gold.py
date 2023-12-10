import numpy

from tools.numpy_tools import str_values_only

grid = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        grid.append(list(line))

grid = numpy.array(grid, dtype=str)
# coordinates are in "southing" and "easting" from the north-west-most corner

# Find starting position
starting_position = numpy.argwhere(grid == "S")
assert len(starting_position) == 1  # only 1 starting position
starting_position = tuple(starting_position[0])
print(f"Starting position {starting_position}")

# Find the shape of the pipe covered by S to form a loop
north = grid[starting_position[0]-1, starting_position[1]]
east = grid[starting_position[0], starting_position[1]+1]
south = grid[starting_position[0]+1, starting_position[1]]
west = grid[starting_position[0], starting_position[1]-1]
north_connected = north in ["|", "7", "F"]
east_connected = east in ["-", "J", "7"]
south_connected = south in ["|", "L", "J"]
west_connected = west in ["-", "L", "F"]
assert [north_connected, east_connected, south_connected, west_connected].count(True) == 2
if north_connected and east_connected:
    pipe_at_start = "L"
elif north_connected and south_connected:
    pipe_at_start = "|"
elif north_connected and west_connected:
    pipe_at_start = "J"
elif east_connected and south_connected:
    pipe_at_start = "F"
elif east_connected and west_connected:
    pipe_at_start = "-"
elif south_connected and west_connected:
    pipe_at_start = "7"
else:
    raise RuntimeError()
print(f"Pipe as starting position is {pipe_at_start}")
grid[starting_position[0], starting_position[1]] = pipe_at_start


def adjacent_positions(position: tuple[int, int]) -> list[tuple[int, int]]:
    pipe_at_position = grid[position[0], position[1]]
    if pipe_at_position == '|':
        return [(position[0]-1, position[1]), (position[0]+1, position[1])]
    elif pipe_at_position == '-':
        return [(position[0], position[1]-1), (position[0], position[1]+1)]
    elif pipe_at_position == 'L':
        return [(position[0]-1, position[1]), (position[0], position[1]+1)]
    elif pipe_at_position == 'J':
        return [(position[0]-1, position[1]), (position[0], position[1]-1)]
    elif pipe_at_position == '7':
        return [(position[0]+1, position[1]), (position[0], position[1]-1)]
    elif pipe_at_position == 'F':
        return [(position[0]+1, position[1]), (position[0], position[1]+1)]
    else:
        raise ValueError("Not in pipe")


def move(position: tuple[int, int], previous_position: tuple[int, int]) -> tuple[int, int]:
    adj = adjacent_positions(position)
    if adj[0] == previous_position:
        return adj[1]
    elif adj[1] == previous_position:
        return adj[0]
    raise ValueError(f"{previous_position=} does not seem adjacent to {position=}. Found {adj=}")


# run the loop and only keep pipes for our loop, remove the rest
filtered_grid = numpy.full(shape=grid.shape, fill_value=".")
position = (starting_position[0], starting_position[1])
adj = adjacent_positions(starting_position)
previous_position = adj[0]
while True:
    #print(position)
    filtered_grid[position] = grid[position]
    next_position = move(position, previous_position)
    previous_position = position
    position = next_position
    if position == starting_position:
        break

print(str_values_only(filtered_grid))

num_positions_inside = 0
it = numpy.nditer(grid, flags=['multi_index'])
for _ in it:
    pos = it.multi_index
    if filtered_grid[pos] != ".":
        continue
    cross_count = 0
    half = None
    while pos[1] > 0:
        pos = (pos[0], pos[1]-1)
        if filtered_grid[pos] == "|":
            cross_count += 1
        elif filtered_grid[pos] == "7":
            assert half is None
            half = "above"
        elif filtered_grid[pos] == "J":
            assert half is None
            half = "below"
        elif filtered_grid[pos] == "-":
            assert half is not None
        elif filtered_grid[pos] == "F":
            assert half is not None
            if half == "above":
                half = None
            elif half == "below":
                cross_count += 1
                half = None
        elif filtered_grid[pos] == "L":
            assert half is not None
            if half == "above":
                cross_count += 1
                half = None
            elif half == "below":
                half = None

    assert half is None
    if cross_count % 2 == 1:
        filtered_grid[it.multi_index] = "I"
        num_positions_inside += 1
    else:
        filtered_grid[it.multi_index] = "O"

print()
print(str_values_only(filtered_grid))
print(num_positions_inside)