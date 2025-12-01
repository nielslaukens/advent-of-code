import math
import typing
import heapq

from tools.graph import CostNode, NodeId

NOTHING = object()  # used as None, but without actually being None
# This way, the user can use None as NodeId


HeapQueueWithFindElement = typing.TypeVar("HeapQueueWithFindElement", bound=typing.Hashable)
class HeapQueueWithChange[HeapQueueWithFindElement]:
    def __init__(self):
        self._heap: list[HeapQueueWithFindElement] = []
        self._value: dict[HeapQueueWithFindElement, int] = {}
        self.__lifo_counter = 0

    def _lifo_counter(self) -> int:
        self.__lifo_counter += 1
        return -self.__lifo_counter

    def push(self, element: HeapQueueWithFindElement, value: int) -> None:
        heapq.heappush(self._heap, (value, self._lifo_counter(), element))
        self._value[element] = value

    def pop_with_value(self) -> tuple[HeapQueueWithFindElement, int]:
        correct_value = 1 # bootstrap
        e = (0,)
        while e[0] != correct_value:
            e = heapq.heappop(self._heap)
            correct_value = self._value.get(e[2])
        del self._value[e[2]]
        return e[2], e[0]

    def pop(self) -> HeapQueueWithFindElement:
        return self.pop_with_value()[0]

    def __len__(self) -> int:
        return len(self._heap)

    def __contains__(self, item: HeapQueueWithFindElement) -> bool:
        return item in self._value

    def __getitem__(self, item: int) -> HeapQueueWithFindElement:
        return self._heap[item][2]

    def upsert_value(self, element: HeapQueueWithFindElement, new_value: int) -> None:
        if self._value.get(element) == new_value:
            return
        heapq.heappush(self._heap, (new_value, self._lifo_counter(), element))
        self._value[element] = new_value


if __name__ == "__main__":
    import timeit
    import random

    h = HeapQueueWithChange()
    print(f"Testing correctness of {h.__class__.__name__}...")
    h.push(2, 2)
    h.push(1, 1)
    h.push(0, 0)
    assert 0 in h
    assert 1 in h
    assert 2 in h
    assert 3 not in h
    assert len(h) == 3
    assert h.pop() == 0
    assert len(h) == 2
    assert h.pop() == 1
    assert h.pop() == 2
    assert len(h) == 0

    h = HeapQueueWithChange()
    h.push(2, 2)
    h.push(1, 1)
    h.push(0, 0)
    assert h.pop() == 0
    h.upsert_value(1, 3)
    assert h.pop() == 2
    assert h.pop() == 1
    assert len(h) == 0

    h = HeapQueueWithChange()
    h.push('first', 5)
    h.push('second', 5)
    assert h.pop() == 'second'
    assert h.pop() == 'first'

    print(f"Testing performance of {h.__class__.__name__}...")
    QL = 100_000
    C = 50_000
    changes = [
        (random.randint(0, QL-1), random.randint(0, QL-1))
        for _ in range(C)
    ]
    def change():
        h = HeapQueueWithChange()
        for i in range(QL):
            h.push(i, i)
        for c in changes:
            h.upsert_value(c[0], c[1])
    t = timeit.timeit(change, number=5)
    print(f"Doing {QL} inserts and {C} changes: {t:.3f} seconds")


def find_best_path(
        start_node: NodeId,
        target_node: NodeId,
        edges_from_node: typing.Callable[[NodeId], typing.Iterable[CostNode]],
        lower_bound_of_cost_to_target: typing.Callable[[NodeId], int],
) -> typing.Mapping[NodeId, CostNode]:
    """
    Find the lowest-cost path (e.g. "shortest path") between two nodes in a directed graph,
    given the (outgoing) edges from each node, and a heuristic function that estimates the
    (remaining) cost between the given node and the target.
    Note that the heuristic must be "admissible" (i.e. never under-estimate).

    Note that this only returns a single path between start_node and target_node.
    If you want the cost from/to multiple nodes, consider using Dijkstra instead.
    """
    best_path: dict[NodeId, CostNode] = {
        start_node: CostNode(0, NOTHING),
    }

    unvisited_nodes = HeapQueueWithChange()
    unvisited_nodes.push(start_node, lower_bound_of_cost_to_target(start_node))
    # Stores the estimated total cost to target,
    # so the actual cost so far + the estimated cost for the remainder

    def iteration():
        # Extracted in separate function to get a call-count while profiling
        current_node = unvisited_nodes.pop()
        cost_to_current_node = best_path[current_node].cost

        for next_cost_node in edges_from_node(current_node):
            assert next_cost_node.cost >= 0
            cost_to_next_node_via_node = cost_to_current_node + next_cost_node.cost
            try:
                current_best_cost = best_path[next_cost_node.node].cost
            except KeyError:
                current_best_cost = math.inf

            if cost_to_next_node_via_node < current_best_cost:
                best_path[next_cost_node.node] = CostNode(cost_to_next_node_via_node, current_node)
                unvisited_nodes.upsert_value(
                    next_cost_node.node,
                    cost_to_next_node_via_node + lower_bound_of_cost_to_target(next_cost_node.node)
                )

    while len(unvisited_nodes) > 0:
        if unvisited_nodes[0] == target_node:
            break
        iteration()

    return best_path


if __name__ == '__main__':
    import timeit

    print("Testing correctness...")
    def list_lookup(from_node) -> list[CostNode]:
        out = []
        for node_pair, cost in edges.items():
            if node_pair[0] == from_node:
                out.append(CostNode(cost, node_pair[1]))
        return out

    edges = {
        (0, 1): 1,
        (1, 2): 2,
    }
    path = find_best_path(0, 2, list_lookup, lambda node: 42)
    assert path[2].cost == 3
    assert path[2].node == 1
    assert path[1].cost == 1
    assert path[1].node == 0

    edges = {
        ('0', '1a'): 1,
        ('0', '1b'): 1,
        ('1a', '2'): 2,
        ('1b', '2'): 1,
    }
    path = find_best_path('0', '2', list_lookup, lambda node: 42)
    assert path['2'].cost == 2
    assert path['2'].node == '1b'
    assert path['1b'].cost == 1
    assert path['1b'].node == '0'

    print("Testing performance...")
    GRID_SIZE = (200, 1000)  # tuned to give around 5 seconds of runtime
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

    t = timeit.timeit(lambda: find_best_path(
            (GRID_SIZE[0]-1, GRID_SIZE[1]-1), (0, 0), edges,
            lambda coord: 0,
        ),
        number=3
    )
    print(f"no heuristic: {t:.3f}")

    t = timeit.timeit(lambda: find_best_path(
            (GRID_SIZE[0]-1, GRID_SIZE[1]-1), (0, 0), edges,
            lambda coord: 1*coord[0] + 2*coord[1],
        ),
        number=3,
    )
    print(f"perfect heuristic: {t:.3f}")
