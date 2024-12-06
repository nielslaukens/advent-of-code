import dataclasses
import enum


class GuardDirection(enum.Enum):
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'

    def right_turn(self) -> "GuardDirection":
        if self == GuardDirection.UP:
            return GuardDirection.RIGHT
        elif self == GuardDirection.RIGHT:
            return GuardDirection.DOWN
        elif self == GuardDirection.DOWN:
            return GuardDirection.LEFT
        elif self == GuardDirection.LEFT:
            return GuardDirection.UP
        else:
            raise RuntimeError("Unreachable")


obstacle_coordinates: set[tuple[int, int]] = set()
floor_size: tuple[int, int] = None
guard_start_pos: tuple[int, int] = None
guard_start_dir: GuardDirection = GuardDirection.UP
with open("input.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, char in enumerate(line.strip()):
            if char == "#":
                obstacle_coordinates.add((x, y))
            elif char == '^':
                guard_start_pos = (x, y)
            elif char == '.':
                pass
            else:
                raise RuntimeError(f"Unrecognized map char: {char}")
    floor_size = (x+1, y+1)


@dataclasses.dataclass(frozen=True)
class Guard:
    position: tuple[int, int]  # counting (right, down) from top left corner
    direction: GuardDirection

    def _position_in_front(self) -> tuple[int, int]:
        if self.direction == GuardDirection.UP:
            return self.position[0], self.position[1] - 1
        elif self.direction == GuardDirection.RIGHT:
            return self.position[0] + 1, self.position[1]
        elif self.direction == GuardDirection.DOWN:
            return self.position[0], self.position[1] + 1
        elif self.direction == GuardDirection.LEFT:
            return self.position[0] - 1, self.position[1]
        else:
            raise RuntimeError(f"Unreachable; direction {self.direction}")

    def position_in_front(self) -> tuple[int, int]:
        p = self._position_in_front()
        if not Guard.inside_map(p):
            raise IndexError(p)
        return p

    @staticmethod
    def inside_map(guard_pos: tuple[int, int]) -> bool:
        return 0 <= guard_pos[0] < floor_size[0] and 0 <= guard_pos[1] < floor_size[1]

    def next_pos(self, obstacle_coordinates: set[tuple[int, int]]) -> "Guard":
        next_pos = self.position_in_front()
        if next_pos in obstacle_coordinates:
            rotate = Guard(self.position, self.direction.right_turn())
            return rotate
        return Guard(next_pos, self.direction)


guard_start = Guard(guard_start_pos, guard_start_dir)
guard = guard_start
print(f"floor size: {floor_size}")
print(f"obstacles at: {obstacle_coordinates}")
print(f"Guard: {guard}")


class CycleDetected(Exception):
    pass


class VisitedPositions:
    def __init__(self):
        self.pos: dict[tuple[int, int], set[GuardDirection]] = {}

    def add(self, guard: Guard) -> None:
        self.pos.setdefault(guard.position, set())
        if guard.direction in self.pos[guard.position]:
            raise CycleDetected(self)
        self.pos[guard.position].add(guard.direction)

    def num_positions(self) -> int:
        return len(self.pos)

    def num_positions_and_orientations(self) -> int:
        s = 0
        for o in self.pos.values():
            s += len(o)
        return s

    def __getitem__(self, pos: tuple[int, int]) -> set[GuardDirection]:
        return self.pos[pos]


def walk_until_out_of_map(guard: Guard, obstacle_coordinates: set[tuple[int, int]]) -> VisitedPositions:
    visited = VisitedPositions()
    visited.add(guard)
    try:
        while True:  # until IndexError
            guard = guard.next_pos(obstacle_coordinates)
            visited.add(guard)
    except IndexError as e:
        # exited map
        pass
    return visited


guard_visited_positions = walk_until_out_of_map(guard, obstacle_coordinates)
print(f"Guard visited {guard_visited_positions.num_positions()} different positions "
      f"({guard_visited_positions.num_positions_and_orientations()} including different orientations)")
print()

# We can place obstacles anywhere, but it will only make a difference if
# we're encountering one on our path
# We just calculated all positions that we normally visit. So these are
# the locations where an obstacle would actually make a difference
obstacle_opportunities: set[tuple[int, int]] = set()
possible_obstacle_locations = set(guard_visited_positions.pos.keys())
possible_obstacle_locations.remove(guard_start.position)
for extra_obstacle in possible_obstacle_locations:
    augmented_obstacles = obstacle_coordinates.union({extra_obstacle})
    try:
        walk_until_out_of_map(guard_start, augmented_obstacles)
    except IndexError as e:
        # exited map, this does not result in a loop
        pass
    except CycleDetected as e:
        # loop
        obstacle_opportunities.add(extra_obstacle)

print(f"{len(obstacle_opportunities)} opportunities: {obstacle_opportunities}")
