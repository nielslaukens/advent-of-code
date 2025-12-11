import dataclasses
import typing


NodeId = typing.TypeVar('NodeId', bound=typing.Hashable)


@dataclasses.dataclass(slots=True, eq=True, frozen=True)
class CostNode:
    """
    When used to supply edges, `cost` signifies the cost of this edge, and
    `node` signifies the other end of the edge.
    When returned from find_best_path, `cost` is the *total* cost from
    `start_node` to here, and `node` is the previous node in the best path to
    here.
    """
    cost: int
    node: NodeId

    def __lt__(self, other) -> bool:
        # used by heapq for sorting
        return self.cost < other.cost

    # others for completeness:
    def __gt__(self, other) -> bool:
        return self.cost > other.cost

    def __le__(self, other) -> bool:
        return self.cost <= other.cost

    def __ge__(self, other) -> bool:
        return self.cost >= other.cost

    def __eq__(self, other) -> bool:
        if not isinstance(other, CostNode):
            return False
        return self.cost == other.cost and self.node == other.node


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


def topological_sort_dag(
        edges_from_to: typing.Mapping[NodeId, list[NodeId]],
) -> list[NodeId]:
    """
    Returns the nodes of the Directed Acyclic Graph (DAG) in topological order,
    i.e. a node will be visited only after all it's dependencies (nodes with edges towards this node) are visited

    Note that there are multiple correct orderings, so be careful when writing tests.
    """
    # https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search

    sorted_nodes: list[NodeId] = []

    mark: dict[NodeId, int] = {}  # 0=no, 1=temp, 2=perm
    for f, ts in edges_from_to.items():
        mark[f] = 0
        for t in ts:
            mark[t] = 0

    def visit(n: NodeId) -> None:
        if mark[n] == 2:
            return
        if mark[n] == 1:
            raise ValueError("Loop detected in graph")

        mark[n] = 1

        for m in edges_from_to.get(n, []):
            visit(m)

        mark[n] = 2
        sorted_nodes.insert(0, n)

    while True:
        for n, m in mark.items():
            if m == 0:
                break
        else:
            break
        visit(n)
    return sorted_nodes


def dag_reverse(
        edges_from_to: typing.Mapping[NodeId, list[NodeId]],
) -> typing.Mapping[NodeId, list[NodeId]]:
    """
    Reverse the direction of a Directed Acyclic Graph (DAG).
    """
    rev: dict[NodeId, list[NodeId]] = {}
    for fr, tos in edges_from_to.items():
        for to in tos:
            rev.setdefault(to, []).append(fr)
    return rev


def number_of_paths_between(
        edge_from_to: typing.Mapping[NodeId, list[NodeId]],
        begin: NodeId,
        end: NodeId,
        edge_to_from: typing.Mapping[NodeId, list[NodeId]] = None,
) -> int:
    """
    Count the number of paths between `begin` and `end` in the given graph `edges_from_to`.

    This function needs the reversed graph as well, if the caller already has this, you can pass it in.
    Otherwise it will be calculated here.

    Note that this only returns the *number* of paths, not the actual paths themselves.
    For that, look into the Tree Traversal module
    """
    if edge_to_from is None:
        edge_to_from = dag_reverse(edge_from_to)

    num_paths: dict[NodeId, int] = {
        end: 1,
    }

    for node in topological_sort_dag(edge_to_from):
        for next_node in edge_from_to.get(node, []):
            num_paths[node] = num_paths.get(node, 0) + num_paths.get(next_node, 0)

    return num_paths.get(begin, 0)



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


    dag = {
        3: [4],
        2: [4, 3],
        1: [3, 2],
    }
    nodes = topological_sort_dag(dag)
    assert nodes == [1, 2, 3, 4]
    assert number_of_paths_between(dag, 1, 4) == 3

    dag = {
        1: [2, 3],
        2: [4],
        3: [4],
    }
    nodes = topological_sort_dag(dag)
    assert nodes == [1, 2, 3, 4] or nodes == [1, 3, 2, 4]
    assert number_of_paths_between(dag, 1, 4) == 2

    cyclic_graph = {
        1: [2],
        2: [1],
    }
    try:
        topological_sort_dag(cyclic_graph)
        raise AssertionError("Should raise ValueError")
    except ValueError as e:
        pass
    try:
        number_of_paths_between(cyclic_graph, 1, 2)
        raise AssertionError("Should raise ValueError")
    except ValueError as e:
        pass

    print("done")
