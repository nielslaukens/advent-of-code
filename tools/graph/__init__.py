import typing

NodeId = typing.TypeVar('NodeId', bound=typing.Hashable)


def remove_node(
        edge_costs: typing.Mapping[typing.Tuple[NodeId, NodeId], int],
        node_to_remove: NodeId,
        reconnect_edges: bool = False,
) -> typing.Mapping[typing.Tuple[NodeId, NodeId], int]:
    """
    Removes a node from a graph.
    When reconnect_edges is False (the default), all paths through the deleted Node are deleted as well.
    When reconnect_edges is True, paths through the deleted Node will be re-connected directly
    :param edge_costs: Mapping between edges and the associated cost for this path (from, to)
    :return: Update mapping between edges and the associated cost for this path (from, to)
    """
    new_edge_costs = {}
    inbound_edges = {}
    outbound_edges = {}
    for edge, cost in edge_costs.items():
        src, dst = edge
        if src != node_to_remove and dst != node_to_remove:
            new_edge_costs[edge] = cost
        elif src == node_to_remove and dst == node_to_remove:
            pass
        elif src == node_to_remove:
            outbound_edges[dst] = cost
        elif dst == node_to_remove:
            inbound_edges[src] = cost

    if reconnect_edges:
        for src, in_cost in inbound_edges.items():
            for dst, out_cost in outbound_edges.items():
                if src == dst:
                    continue
                new_edge_costs[(src, dst)] = in_cost + out_cost

    return new_edge_costs


if __name__ == "__main__":
    print("running tests")

    edge_costs = {
        (0, 1): 1,
        (1, 2): 2,
    }
    nec = remove_node(edge_costs, 1)
    assert nec == {}
    nec = remove_node(edge_costs, 1, reconnect_edges=True)
    assert nec == {(0, 2): 3}


    edge_costs = {
        (0, 1): 1,
        (1, 0): 10,
        (1, 2): 2,
        (2, 1): 20,
    }
    nec = remove_node(edge_costs, 1)
    assert nec == {}
    nec = remove_node(edge_costs, 1, reconnect_edges=True)
    assert nec == {(0, 2): 3, (2, 0): 30}

    print("done")
