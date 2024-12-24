edges: dict[str, set[str]] = {}

# Node, edges are bi-directional / non-directional
with open("input.txt") as f:
    for line in f:
        nodea, nodeb = line.strip().split('-')
        edges.setdefault(nodea, set()).add(nodeb)
        edges.setdefault(nodeb, set()).add(nodea)

#print(edges)

lan_parties: set[frozenset[str]] = set()
for computer, neighbors in edges.items():
    my_neighbourhood = neighbors.copy()
    for neighbor in neighbors:
        their_neighborhood = edges[neighbor]
        common_neighbors = my_neighbourhood.intersection(their_neighborhood)
        for common_neighbor in common_neighbors:
            lan_parties.add(frozenset([computer, neighbor, common_neighbor]))

for party in lan_parties:
    print(party)
print(len(lan_parties))
print()

parties_with_t = 0
for party in lan_parties:
    any_starts_with_t = False
    for computer in party:
        if computer.startswith('t'):
            any_starts_with_t = True
            break
    if any_starts_with_t:
        print(party)
        parties_with_t += 1
print(parties_with_t)
