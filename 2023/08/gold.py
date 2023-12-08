import math

from tools.cycle_detect import CycleDetector, CycleInfo, lcm_with_offset

nodes: dict[str, dict[str, str]] = {}
with open("input.txt", "r") as f:
    instructions = list(f.readline().rstrip())
    empty_line = f.readline().strip()
    assert empty_line == ""
    for line in f:
        line = line.rstrip()
        node_name, _ = line.split(" = ")
        assert _.startswith("(")
        assert _.endswith(")")
        left_node, right_node = _[1:-1].split(", ")
        assert node_name not in nodes
        nodes[node_name] = {"L": left_node, "R": right_node}


class InstructionLoop:
    def __init__(self, instructions: list[str]):
        self.instructions = instructions
        self.len_instructions = len(instructions)
        self.i = 0

    def __next__(self) -> str:
        _ = self.instructions[self.i]
        self.i += 1
        if self.i == self.len_instructions:
            self.i = 0
        return _


def naive(stop_at: int = None):
    """
    Works, but way too slow
    """
    positions = list(filter(lambda node_name: node_name.endswith('A'), nodes.keys()))
    len_positions = len(positions)
    len_instructions = len(instructions)
    step = 0
    arrived = False
    while not arrived:
        instruction = instructions[step % len_instructions]
        print(step, positions)
        step += 1
        arrived = True
        for i in range(len_positions):
            _ = nodes[positions[i]][instruction]
            positions[i] = _
            if not _[2] == 'Z':
                arrived = False

        if step == stop_at:
            break
        if step % 1_000_000 == 0:
            print(step)

    print(f"step {step}: {positions}")


def try2():
    # We'll probably run in circles until all positions are at an end
    # figure out what cycle time we have for each dimension
    instructions_loop = InstructionLoop(instructions)
    positions = list(filter(lambda node_name: node_name.endswith('A'), nodes.keys()))
    pos_history = [CycleDetector((pos, instructions_loop.i)) for pos in positions]
    step = 0
    cycles: list[CycleInfo] = [None for _ in positions]
    while any(map(lambda c: c is None, cycles)):
        instruction = next(instructions_loop)
        step += 1
        if step % 1000 == 0:
            print(f"{step=}")
            for dim, ph in enumerate(pos_history):
                cycle = ph.scan()
                if cycle is not None:
                    cycles[dim] = cycle

        for dim, position in enumerate(positions):
            new_position = nodes[position][instruction]
            pos_history[dim].append((new_position, instructions_loop.i))
            positions[dim] = new_position

    print(cycles)
    print("cycle lengths ", [_.cycle_length for _ in cycles])

    # now see where our end-states are in the cycles
    end_states = [[] for _ in positions]
    for dim in range(len(positions)):
        for i in range(cycles[dim].first_occurrence, cycles[dim].second_occurrence):
            if pos_history[dim].history[i][0].endswith('Z'):
                end_states[dim].append(i)

    assert all(map(lambda _: len(_) == 1, end_states))  # single end_state in each cycle
    end_states = list(map(lambda _: _[0], end_states))
    print("end states ", end_states)

    assert [_.cycle_length for _ in cycles] == end_states  # I don't know if this is mathematically guaranteed to be the case...

    lcm = math.lcm(*end_states)
    print(lcm)


#naive(14893+3*(14895-2))
try2()
