from functools import reduce

LIMIT = 1000
with open("input.txt") as f:
    boxes: list[tuple[int, int, int]] = [
        tuple(int(coord) for coord in line.split(','))
        for line in f.read().splitlines()
    ]

#print(boxes)

def distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    # Problem specifies Euclidian distance,
    # but since we're only interested in the order of the distances,
    # we can omit the square root to speed things up
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2

distances: dict[tuple[tuple[int, int, int], tuple[int, int, int]], int] = {}
for i, a in enumerate(boxes):
    for j, b in enumerate(boxes):
        if j <= i:
            continue
        distances[(a, b)] = distance(a, b)

closest = sorted(distances.keys(), key=lambda cc: distances[cc])

max_circuit = 0
circuits: dict[tuple[int, int, int], int] = {}
for i, box_pair in enumerate(closest):
    if i == LIMIT:
        break
    box_a, box_b = box_pair
    if box_a not in circuits and box_b not in circuits:
        max_circuit += 1
        circuits[box_a] = max_circuit
        circuits[box_b] = max_circuit
        print(f"linking {box_a} to {box_b} as circuit {max_circuit}")
    elif box_a in circuits and box_b not in circuits:
        circuits[box_b] = circuits[box_a]
        print(f"joining {box_b} to circuit {circuits[box_a]} of {box_a}")
    elif box_a not in circuits and box_b in circuits:
        circuits[box_a] = circuits[box_b]
        print(f"joining {box_a} to circuit {circuits[box_b]} of {box_b}")
    elif box_a in circuits and box_b in circuits:
        if circuits[box_a] == circuits[box_b]:
            print(f"{box_a} and {box_b} are already connected in circuit {circuits[box_a]}")
            pass  # already connected?
        else:
            new = circuits[box_a]
            old = circuits[box_b]
            print(f"connecting circuit {box_a} to {box_b}, connecting circuit {new} with {old}")
            for k, v in circuits.items():
                if v == old:
                    circuits[k] = new
    else:
        raise RuntimeError("missed case")


print()
circuits_reversed = {}
for k, v in circuits.items():
    circuits_reversed.setdefault(v, []).append(k)
circuit_length = {}
for k, v in circuits_reversed.items():
    print(f"circuit {k} : {len(v)} {v}")
    circuit_length[k] = len(v)

size_of_circuits = sorted(circuit_length.values(), reverse=True)
print(reduce(lambda acc, e: acc * e, size_of_circuits[:3], 1))
