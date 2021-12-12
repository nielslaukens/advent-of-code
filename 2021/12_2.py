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


def num_2_visits_lc(l: list) -> int:
    v = {}
    for e in l:
        if is_lower_case(e):
            v[e] = v.get(e, 0) + 1
    two_or_more = 0
    for num in v.values():
        if num >= 2:
            two_or_more += 1
    return two_or_more


def find_paths(current_node: str, path_so_far: typing.List[str]):
    if current_node == 'end':
        return [path_so_far]

    num_visits_per_cave = {}
    for cave in path_so_far:
        num_visits_per_cave[cave] = num_visits_per_cave.get(cave, 0) + 1

    paths = []
    for next_cave in edges_per_node[current_node]:
        if is_upper_case(next_cave):
            # Upper case: visit as many times as you want
            may_visit = True
        elif next_cave == 'start':
            # Never visit start (again)
            may_visit = False
        elif next_cave == 'end':
            # Always visit end (and stop there)
            may_visit = True
        elif num_visits_per_cave.get(next_cave, 0) < 1:
            # this (lower case) cave has not been visited
            may_visit = True
        elif num_2_visits_lc(path_so_far) < 1:
            # no lower case cave has been visited twice yet,
            # allow visiting this nexc_cave twice
            may_visit = True
        else:
            may_visit = False

        # print(f"{path_so_far} considering {next_cave}: {may_visit} {num_2_visits_lc(path_so_far)}")

        if may_visit:
            paths_via_next_cave = find_paths(next_cave, path_so_far + [next_cave])
            paths.extend(paths_via_next_cave)
    return paths


paths = find_paths('start', ['start'])
for path in paths:
    print(','.join(path))
print(f"{len(paths)} paths")
