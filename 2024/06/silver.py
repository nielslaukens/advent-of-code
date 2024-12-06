import numpy as np

with open("input.txt", "r") as f:
    floor = np.array([
        list(line.strip())
        for line in f.readlines()
    ])

print(floor)
guard_pos = np.where(floor == '^')
guard_pos = int(guard_pos[0][0]), int(guard_pos[1][0])
guard_dir = '^'
print(guard_pos, guard_dir)
floor[guard_pos] = 'X'  # mark visited


def take_step(guard_pos: tuple[int, int], guard_dir: str) -> tuple[int, int]:
    if guard_dir == '^':
        return guard_pos[0] - 1, guard_pos[1]
    elif guard_dir == '>':
        return guard_pos[0], guard_pos[1] + 1
    elif guard_dir == 'v':
        return guard_pos[0] + 1, guard_pos[1]
    elif guard_dir == '<':
        return guard_pos[0], guard_pos[1] - 1
    else:
        raise RuntimeError(f"Unreachable; direction {guard_dir}")


def inside_map(guard_pos: tuple[int, int]) -> bool:
    return 0 <= guard_pos[0] < floor.shape[0] and 0 <= guard_pos[1] < floor.shape[1]


while True:
    new_guard_pos = take_step(guard_pos, guard_dir)
    if not inside_map(new_guard_pos):
        break

    if floor[new_guard_pos] == '#':
        # obstacle, turn 90º instead
        if guard_dir == '^':
            guard_dir = '>'
        elif guard_dir == '>':
            guard_dir = 'v'
        elif guard_dir == 'v':
            guard_dir = '<'
        elif guard_dir == '<':
            guard_dir = '^'
        else:
            raise RuntimeError("Unreachable")
        new_guard_pos = take_step(guard_pos, guard_dir)
    elif floor[new_guard_pos] in {'.', 'X'}:
        floor[new_guard_pos] = 'X'
        guard_pos = new_guard_pos
    else:
        raise RuntimeError("Unreachable")

print(floor)
print(np.count_nonzero(floor == 'X'))
