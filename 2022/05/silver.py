import dataclasses
import re


@dataclasses.dataclass()
class Move:
    num_of_crates: int
    source_stack: int
    dest_stack: int


stacks = []
move_instructions = []

input_state = 'stacks'
with open('input.txt', 'r') as f:
    for line in f:
        line = line.rstrip()
        if input_state == 'stacks':
            if line[1] == '1':
                input_state = 'empty_line'
                # ignore numbers line
            else:
                i = 0
                while 4*i < len(line):
                    crate = line[4*i + 1]
                    while len(stacks) < i+1:
                        stacks.append([])
                    if crate != ' ':
                        stacks[i].insert(0, crate)
                    i += 1

        elif input_state == 'empty_line':
            assert line == ""
            input_state = 'move'
        elif input_state == 'move':
            match = re.match(r'move (\d+) from (\d+) to (\d+)', line)
            assert match
            m = Move(int(match.group(1)),
                     int(match.group(2)),
                     int(match.group(3)))
            move_instructions.append(m)


def print_stacks(stacks):
    for i, s in enumerate(stacks):
        print(f"{i+1} : {s}")


def move(src_1: int, dst_1: int) -> None:
    crate = stacks[src_1-1].pop()
    stacks[dst_1-1].append(crate)


print_stacks(stacks)
print()

for m in move_instructions:
    print(f"Moving {m.num_of_crates} crates from {m.source_stack} to {m.dest_stack}")
    for i in range(m.num_of_crates):
        move(m.source_stack, m.dest_stack)
    print_stacks(stacks)
    print()

top = ''
for s in stacks:
    top += s[-1]

print(f"TOP: {top}")
