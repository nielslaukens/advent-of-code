
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
        nodes[node_name] = {"L": left_node, "R": right_node}

position = 'AAA'
steps = 0
while position != 'ZZZ':
    steps += 1
    current_instruction = instructions.pop(0)
    instructions.append(current_instruction)  # loop around
    new_position = nodes[position][current_instruction]
    print(f"step {steps}: {position}: going {current_instruction} to {new_position}")
    position = new_position
