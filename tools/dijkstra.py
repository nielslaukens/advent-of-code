import dataclasses
import typing


@dataclasses.dataclass
class NextHop:
    next_hop: typing.Any
    cost: int


def _dijkstra_iteration(
        nodes: typing.Mapping[typing.Any, NextHop],
        outgoing_edges: typing.Mapping[typing.Any, typing.Mapping[typing.Any, int]],
) -> int:
    """nodes is updated in-place"""
    nodes_changed = 0
    for node in nodes.keys():
        for next_node, cost in outgoing_edges[node].items():
            if nodes[next_node].cost is None:
                continue
            cost_via_next_node = cost + nodes[next_node].cost
            if nodes[node].cost is None or cost_via_next_node < nodes[node].cost:  # found (better) path
                nodes[node].next_hop = next_node
                nodes[node].cost = cost_via_next_node
                nodes_changed += 1

    return nodes_changed


def dijkstra(
        edge_costs: typing.Mapping[typing.Tuple[typing.Any, typing.Any], int],
        nodes_to_calculate_to: typing.Any,
) -> typing.Mapping[typing.Any, NextHop]:
    """
    Calculate costs between nodes, multi-hop
    :param edge_costs: Mapping between edges and the associated cost for this path
    :param nodes_to_calculate_to: Calculate costs to this destination node
    :return: Cost & path from each node to the given destination node
    """
    nodes = {}
    outgoing_edges = {}
    for node_from, node_to in edge_costs.keys():
        nodes[node_from] = NextHop(None, None)
        nodes[node_to] = NextHop(None, None)
        outgoing_edges.setdefault(node_from, {})
        outgoing_edges.setdefault(node_to, {})
        outgoing_edges[node_from][node_to] = edge_costs[(node_from, node_to)]

    if nodes_to_calculate_to not in nodes:
        raise ValueError(f"Could not find node `{repr(nodes_to_calculate_to)}` in edge_costs")
    nodes[nodes_to_calculate_to].cost = 0

    while _dijkstra_iteration(nodes, outgoing_edges):
        pass

    return nodes


if __name__ == "__main__":
    edges = {
        (0, 1): 1,
        (1, 2): 2,
    }
    costs = dijkstra(edges, 2)
    assert costs[1].next_hop == 2
    assert costs[1].cost == 2
    assert costs[0].next_hop == 1
    assert costs[0].cost == 3


    edges = {
        ('0', '1a'): 1,
        ('0', '1b'): 1,
        ('1a', '2'): 2,
        ('1b', '2'): 1,
    }
    costs = dijkstra(edges, '2')
    assert costs['0'].next_hop == '1b'
    assert costs['0'].cost == 2
