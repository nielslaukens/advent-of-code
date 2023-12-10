import numpy

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


# run the loop and count distance
distance = 0
grid_distance = numpy.full(shape=grid.shape, fill_value=None)
grid_distance[starting_position[0], starting_position[1]] = distance
positions = [(starting_position[0], starting_position[1]), (starting_position[0], starting_position[1])]
adj = adjacent_positions(starting_position)
previous_positions = [adj[0], adj[1]]


def update_with_min(grid, pos: tuple[int, int], value):
    if grid[pos] is None:
        grid[pos] = value
    elif grid[pos] > value:
        grid[pos] = value
    # else: leave grid


while True:
    #print(positions)
    next_positions = [
        move(positions[0], previous_positions[0]),
        move(positions[1], previous_positions[1]),
    ]
    previous_positions = positions
    positions = next_positions
    if grid_distance[positions[0]] != None and grid_distance[positions[1]] != None:
        break
    distance += 1
    update_with_min(grid_distance, positions[0], distance)
    update_with_min(grid_distance, positions[1], distance)

print(grid_distance)
print(distance)
