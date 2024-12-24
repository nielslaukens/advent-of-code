import typing

neighborhoods: set[frozenset[str]] = set()
edges: dict[str, set[str]] = {}
# Node, edges are bi-directional / non-directional
with open("input.txt") as f:
    for line in f:
        a, b = line.strip().split('-')
        neighborhoods.add(frozenset([a, b]))
        edges.setdefault(a, set()).add(b)
        edges.setdefault(b, set()).add(a)

#print(edges)


def find_common_neighbors(computers: typing.Iterable[str]) -> set[str]:
    it = iter(computers)
    try:
        first_computer = next(it)
    except StopIteration:
        raise ValueError()

    candidates = edges[first_computer].copy()
    for next_computer in it:
        candidates.intersection_update(edges[next_computer])
    return candidates


def grow_neighborhood(computers: frozenset[str]) -> set[frozenset[str]]:
    common_neighbors = find_common_neighbors(computers)
    neighborhoods = set()
    for neighbor in common_neighbors:
        neighborhoods.add(frozenset([*computers, neighbor]))
    return neighborhoods


neighborhoods_final: set[frozenset[str]] = set()
while len(neighborhoods) > 0:
    neighborhoods_that_grew: set[frozenset[str]] = set()
    for neighborhood in neighborhoods:
        grown = grow_neighborhood(neighborhood)
        if len(grown) > 0:
            neighborhoods_that_grew.update(grown)
        else:
            neighborhoods_final.add(neighborhood)
    neighborhoods = neighborhoods_that_grew

largest_neighborhood = {}
for neighborhood in neighborhoods_final:
    if len(neighborhood) > len(largest_neighborhood):
        largest_neighborhood = neighborhood

print(','.join(sorted(largest_neighborhood)))
