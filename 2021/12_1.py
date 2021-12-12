import typing

with open("12.input.txt", "r") as f:
    edges = [
        tuple(line.strip().split('-'))
        for line in f.readlines()
    ]

edges_per_node = {}
for node1, node2 in edges:
    edges_per_node.setdefault(node1, set())
    edges_per_node.setdefault(node2, set())
    edges_per_node[node1].add(node2)
    edges_per_node[node2].add(node1)


def is_lower_case(s: str) -> bool:
    return s.lower() == s


def is_upper_case(s: str) -> bool:
    return s.upper() == s


def find_paths(current_node: str, path_so_far: typing.List[str]):
    if current_node == 'end':
        return [path_so_far]

    paths = []
    for next_cave in edges_per_node[current_node]:
        if next_cave not in path_so_far or is_upper_case(next_cave):
            paths_via_next_cave = find_paths(next_cave, path_so_far + [next_cave])
            paths.extend(paths_via_next_cave)
    return paths


paths = find_paths('start', ['start'])
for path in paths:
    print(path)
print(f"{len(paths)} paths")
