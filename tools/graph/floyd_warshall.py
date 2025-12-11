import typing

from tools.graph import NodeId


def floyd_warshall(
        edge_costs: typing.Mapping[typing.Tuple[NodeId, NodeId], int],
) -> typing.Mapping[NodeId, typing.Mapping[NodeId, int]]:
    """
    Calculate the lowest cost between all node-pairs from the listed edge costs.
    :param edge_costs: Mapping between edges and the associated cost for this path (from, to)

    Note that this does NOT return the path to take to achieve that cost;
    consider using Dijkstra or A* instead.

    Complexity: O(n^3)
    """
    cost_from_to: dict[NodeId, dict[NodeId, int | None]] = {}
    for edge, cost in edge_costs.items():
        src, dst = edge
        cost_from_to.setdefault(src, {})[src] = 0
        cost_from_to.setdefault(dst, {})[dst] = 0
        cost_from_to[src][dst] = cost
    for k in cost_from_to.keys():
        for i in cost_from_to.keys():
            for j in cost_from_to.keys():
                known_cost = cost_from_to.get(i, {}).get(j)
                try:
                    maybe_better = cost_from_to[i][k] + cost_from_to[k][j]
                except KeyError:
                    maybe_better = None
                if maybe_better is not None and (
                        known_cost is None or maybe_better < known_cost
                ):
                    cost_from_to[i][j] = maybe_better
    return cost_from_to


if __name__ == "__main__":
    print("Running tests")

    edges = {
        (0, 1): 1,
        (1, 2): 2,
    }
    costs = floyd_warshall(edges)
    assert costs[0][2] == 3
    assert 1 not in costs[2]
    assert 0 not in costs[2]

    edges = {
        ('0', '1a'): 1,
        ('0', '1b'): 1,
        ('1a', '2'): 2,
        ('1b', '2'): 1,
    }
    costs = floyd_warshall(edges)
    assert costs['0']['2'] == 2
    assert '1a' not in costs['2']
    assert '1b' not in costs['2']
    assert '0' not in costs['2']

    print("done")
