import dataclasses
import itertools


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


def expand_int(a: int, prefix: str, length: int) -> dict[str, bool]:
    out = {
        f"{prefix}{i:02d}": v == "1"
        for i, v in enumerate(reversed(bin(a)[2:]))
    }
    for i in range(len(out), length):
        out[f"{prefix}{i:02d}"] = False
    return out


def compact_int(d: dict[str, bool]) -> int:
    return int(''.join((
        "1" if d[wire] else "0"
        for wire in sorted(d.keys(), reverse=True)
    )), 2)


def deterministic_gates(wires: dict[str, bool], gates: dict[str, Gate]) -> list[tuple[str, Gate]]:
    solved_wires: dict[str, bool] = wires.copy()
    unsolved_gates: dict[str, Gate] = gates.copy()
    solved_gates: list[tuple[str, Gate]] = []

    while len(unsolved_gates) > 0:
        gates_to_remove = []
        for output, gate in unsolved_gates.items():
            try:
                _ = solved_wires[gate.inputs[0]] + solved_wires[gate.inputs[1]]
                solved_wires[output] = True  # whatever
                solved_gates.append((output, gate))
                gates_to_remove.append(output)
            except KeyError:
                pass

        if len(gates_to_remove) == 0:
            raise ValueError("Unsolvable")
        for g in gates_to_remove:
            del unsolved_gates[g]
    return solved_gates


def run_gates(gates: list[tuple[str, Gate]], x: int, y: int) -> tuple[int, list[tuple[str, bool]]]:
    solved_wires: dict[str, bool] = wires.copy()
    solved_gates: list[tuple[str, bool]] = []

    x = expand_int(x, "x", len_x)
    y = expand_int(y, "y", len_y)
    solved_wires.update(x)
    solved_wires.update(y)

    for output, gate in gates:
        if gate.type == 'AND':
            result = solved_wires[gate.inputs[0]] and solved_wires[gate.inputs[1]]
            solved_gates.append((output, result))
            solved_wires[output] = result
        elif gate.type == 'OR':
            result = solved_wires[gate.inputs[0]] or solved_wires[gate.inputs[1]]
            solved_gates.append((output, result))
            solved_wires[output] = result
        elif gate.type == 'XOR':
            result = solved_wires[gate.inputs[0]] != solved_wires[gate.inputs[1]]
            solved_gates.append((output, result))
            solved_wires[output] = result
        else:
            raise RuntimeError(f"Unknown gate {gate.type}")

    result = compact_int({k: v for k, v in solved_wires.items() if k.startswith('z')})
    return result, solved_gates


def swap_gates(swaps: list[tuple[str, str]]) -> dict[str, Gate]:
    swaps_ = {}
    for a, b in swaps:
        assert a not in swaps_
        swaps_[a] = b
        assert b not in swaps_
        swaps_[b] = a
    new_gates = {}
    for output, gate in gates.items():
        possibly_swapped_output = swaps_.get(output, output)
        new_gates[possibly_swapped_output] = gate
    return new_gates


def diff(a: list[tuple[str, bool]], b: list[tuple[str, bool]]) -> list[str]:
    out = []
    assert len(a) == len(b)
    for i, gv in enumerate(a):
        gate_a = a[i][0]
        gate_b = b[i][0]
        assert gate_a == gate_b
        value_a = a[i][1]
        value_b = b[i][1]
        if value_a != value_b:
            out.append(gate_a)
    return out


def trace_input(gates: dict[str, Gate], wire: str) -> list[str]:
    out = []
    try:
        inputs = gates[wire].inputs
        out.extend(inputs)
        for inp in inputs:
            out.extend(trace_input(gates, inp))
        return out
    except KeyError:
        return out


def errors(swaps: list[tuple[str, str]]):
    out = {}
    dgates = deterministic_gates(wires, swap_gates(swaps))
    zero = run_gates(dgates, 0, 0)
    for bit in range(len_x):
        one_a = run_gates(dgates, 2**bit, 0)
        one_b = run_gates(dgates, 0, 2**bit)
        assert one_a == one_b
        diff_ = diff(zero[1], one_a[1])

        zbit = f"z{bit:02d}"
        if zbit not in diff_:
            out[zbit] = (diff_, trace_input(gates, zbit))

        # if sum(1 for gate in diff_a if gate.startswith('z') and gate != zbit) \
        #         or sum(1 for gate in diff_b if gate.startswith('z') and gate != zbit):
        #     print(f"Wrong zbit in {bit} output: {diff_a}  {diff_b}")
    return out


errors_orig = errors([])
for zbit, error_info in errors_orig.items():
    inbit_influence, zbit_input = error_info
    print(f"{zbit} : {inbit_influence} {zbit_input}")

    for a, b in itertools.product(inbit_influence, zbit_input):
        if a == b:
            continue
        try:
            errors_try = errors([(a, b)])
            print(f"Swapped {a} <-> {b}; {errors_try.get(zbit)}")
        except ValueError:
            pass
    break