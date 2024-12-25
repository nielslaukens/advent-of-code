import dataclasses


@dataclasses.dataclass
class Gate:
    inputs: list[str]
    type: str


gates: dict[str, Gate] = {}
wires: dict[str, bool] = {}

state = "wires"
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line == "":
            state = "gates"
            continue
        if state == "wires":
            wire_name, value = line.split(": ")
            wires[wire_name] = value == "1"
        elif state == "gates":
            op, output = line.split(' -> ')
            a, gate, b = op.split(' ')
            gates[output] = Gate([a, b], gate)
        else:
            raise RuntimeError()

len_x = sum(1 for key in wires.keys() if key.startswith('x'))
len_y = sum(1 for key in wires.keys() if key.startswith('y'))
assert len_x == len_y
len_z = sum(1 for key in gates.keys() if key.startswith('z'))
assert len_z == len_x + 1

o = []
p = []
for i in range(len_z):
    zbit = f"z{i:02d}"
    todo = [zbit]
    while todo:
        _ = todo.pop(0)
        if _ in p:
            continue
        elif _ in gates:
            o.append(f"{gates[_].inputs[0]} {gates[_].type} {gates[_].inputs[1]} -> {_}")
            p.append(_)
            todo.extend(gates[_].inputs)
        else:
            pass

for j in o:
    print(j)

# solved manually
