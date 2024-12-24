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

print(wires)
print(gates)
while len(gates) > 0:
    solved_gates = []
    for output, gate in gates.items():
        try:
            if gate.type == 'AND':
                wires[output] = wires[gate.inputs[0]] and wires[gate.inputs[1]]
            elif gate.type == 'OR':
                wires[output] = wires[gate.inputs[0]] or wires[gate.inputs[1]]
            elif gate.type == 'XOR':
                wires[output] = wires[gate.inputs[0]] != wires[gate.inputs[1]]
            else:
                raise RuntimeError(f"Unknown gate {gate.type}")
            solved_gates.append(output)
        except KeyError:
            pass

    for solved_gate in solved_gates:
        del gates[solved_gate]

z_wires = {
    k: v
    for k, v in wires.items()
    if k.startswith('z')
}
print(z_wires)
z_value = [
    wires[k]
    for k in sorted(z_wires.keys(), reverse=True)
]
out = 0
for i in range(len(z_value)):
    out *= 2
    out += 1 if z_value[i] else 0
print(z_value)
print(out)
