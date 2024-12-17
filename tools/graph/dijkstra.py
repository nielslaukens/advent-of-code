import dataclasses
import typing


NodeId = typing.TypeVar('NodeId', bound=typing.Hashable)


@dataclasses.dataclass
class NextHop:
    next_hop: NodeId | None
    cost: int | None


def dijkstra(
        edge_costs: typing.Mapping[typing.Tuple[NodeId, NodeId], int],
        node_to_calculate_to: NodeId,
) -> typing.Mapping[NodeId, NextHop]:
    """
    Calculate costs between nodes, multi-hop
    :param edge_costs: Mapping between edges and the associated cost for this path (from, to)
    :param node_to_calculate_to: Calculate costs to this destination node
    :return: Cost & path from each node to the given destination node
    """
    nodes: typing.Dict[typing.Hashable, NextHop] = {}
    outgoing_edges: dict[NodeId, dict[NodeId, int]] = {}  # outgoing_edges[from][to] = cost
    inbound_edges: dict[NodeId, dict[NodeId, int]] = {}  # inbound_edges[to][from] = cost
    for node_from, node_to in edge_costs.keys():
        nodes[node_from] = NextHop(None, None)
        nodes[node_to] = NextHop(None, None)
        outgoing_edges.setdefault(node_from, {})
        outgoing_edges.setdefault(node_to, {})
        outgoing_edges[node_from][node_to] = edge_costs[(node_from, node_to)]
        inbound_edges.setdefault(node_from, {})
        inbound_edges.setdefault(node_to, {})
        inbound_edges[node_to][node_from] = edge_costs[(node_from, node_to)]

    if node_to_calculate_to not in nodes:
        raise ValueError(f"Could not find node `{repr(node_to_calculate_to)}` in edge_costs")
    nodes[node_to_calculate_to].cost = 0

    def iteration():
        # Extracted in separate function to get a call-count while profiling
        nodes_to_recalculate = set()
        for changed_node in nodes_changed_previous_iteration:
            for node in inbound_edges[changed_node].keys():  # nodes connecting to the changed node
                nodes_to_recalculate.add(node)

        nodes_changed = set()
        for node in nodes_to_recalculate:
            for next_node, cost in outgoing_edges[node].items():
                if nodes[next_node].cost is None:
                    # no path (yet) via next_node
                    continue
                cost_via_next_node = cost + nodes[next_node].cost
                if nodes[node].cost is None or cost_via_next_node < nodes[node].cost:  # found (better) path
                    nodes[node].next_hop = next_node
                    nodes[node].cost = cost_via_next_node
                    nodes_changed.add(node)

        return nodes_changed

    nodes_changed = {node_to_calculate_to}
    while len(nodes_changed) > 0:
        nodes_changed_previous_iteration = nodes_changed
        nodes_changed = iteration()

    return nodes


if __name__ == "__main__":
    print("Running tests")

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

    print("Done")
