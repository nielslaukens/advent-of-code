import collections.abc
import dataclasses
import heapq
import math
import typing


NodeId = typing.TypeVar('NodeId', bound=typing.Hashable)

_NOTHING = object()  # used as None, but without actually being None
# This way, the user can use None as NodeId


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

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __ge__(self, other):
        return self.cost >= other.cost


def find_best_path(
        start_node: NodeId,
        edges_from_node: collections.abc.Callable[[NodeId], typing.Iterable[CostNode]],
        target_node: NodeId = _NOTHING,
) -> typing.Mapping[NodeId, CostNode]:
    """
    Explores a graph, starting at start_node.
    For each node/vertex, explores the edges that start from this node given by
    edges_from_node(node). This callable should return both the cost for this
    edge, and the node on the other side of the edge.

    Returns a mapping of each discovered node to the (total) cost and previous
    node in the path. That way you can trace back the path from an arbitrary
    node to the start node.

    Optionally, the algorithm can stop once it found the best path to
    target_node, without exploring the graph further.

    Note that you can also run this algorithm "backwards": You can find the
    best path *to* a target node, *from* all nodes in the graph. To do so,
    supply your target as `start_node`, and return edges *to* each node in the
    edges_from_node() callable, which will be traversed "backwards".
    """
    best_path: dict[NodeId, CostNode] = {start_node: CostNode(0, None)}
    unvisited_nodes: list[CostNode] = [CostNode(0, start_node)]  # heapq, but stored as list

    def iteration():
        # Extracted in separate function to get a call-count while profiling
        current_costnode = heapq.heappop(unvisited_nodes)
        cost_to_current_node = best_path[current_costnode.node].cost
        for next_cost_node in edges_from_node(current_costnode.node):
            cost_to_next_node_via_node = cost_to_current_node + next_cost_node.cost
            try:
                current_best_cost = best_path[next_cost_node.node].cost
            except KeyError:
                heapq.heappush(unvisited_nodes, CostNode(cost_to_next_node_via_node, next_cost_node.node))
                current_best_cost = math.inf
            if cost_to_next_node_via_node < current_best_cost:
                best_path[next_cost_node.node] = CostNode(cost_to_next_node_via_node, current_costnode.node)

    while len(unvisited_nodes) > 0:
        if unvisited_nodes[0].node == target_node:
            break
        iteration()

    return best_path


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
    inbound_nodes: dict[NodeId, list[CostNode]] = {}
    for node_pair, cost in edge_costs.items():
        inbound_nodes.setdefault(node_pair[1], [])
        inbound_nodes[node_pair[1]].append(CostNode(cost, node_pair[0]))
    def list_lookup(node: int) -> list[CostNode]:
        return inbound_nodes.get(node, [])

    return {
        k: NextHop(v.node, v.cost)
        for k, v in find_best_path(node_to_calculate_to, list_lookup).items()
    }


if __name__ == "__main__":
    import timeit

    print("Testing correctness...")
    def list_lookup(to_node: int) -> list[CostNode]:
        out = []
        for node_pair, cost in edges.items():
            if node_pair[1] == to_node:
                out.append(CostNode(cost, node_pair[0]))
        return out

    edges = {
        (0, 1): 1,
        (1, 2): 2,
    }
    costs = dijkstra(edges, 2)
    assert costs[1].next_hop == 2
    assert costs[1].cost == 2
    assert costs[0].next_hop == 1
    assert costs[0].cost == 3

    costs = find_best_path(2, list_lookup)
    assert costs[1].node == 2
    assert costs[1].cost == 2
    assert costs[0].node == 1
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

    costs = find_best_path('2', list_lookup)
    assert costs['0'].node == '1b'
    assert costs['0'].cost == 2


    print("Testing performance...")
    GRID_SIZE = (100, 1000)
    def edges(coord: tuple[int, int]) -> typing.Generator[CostNode, None, None]:
        # 2D-grid of nodes, edges are up/down/left/right, each with different cost
        if coord[0] > 0:
            yield CostNode(1, (coord[0] - 1, coord[1]))
        if coord[1] > 0:
            yield CostNode(2, (coord[0], coord[1] - 1))
        if coord[0] < GRID_SIZE[0]:
            yield CostNode(3, (coord[0] + 1, coord[1]))
        if coord[1] < GRID_SIZE[1]:
            yield CostNode(4, (coord[0], coord[1] + 1))
    rendered_edges = {}
    for x in range(GRID_SIZE[0]):
        for y in range(GRID_SIZE[1]):
            for neighbor in edges((x, y)):
                rendered_edges[((x, y), neighbor.node)] = neighbor.cost

    t = timeit.timeit(lambda: dijkstra(rendered_edges, (0, 0)), number=3)
    print(f"dijkstra(): {t:.3f}")
    t = timeit.timeit(lambda: find_best_path((0, 0), edges), number=3)
    print(f"find_best_path(): {t:.3f}")
