"""
Tree traversal Generators.

Instead of pruning branches in the `branches()` callable, you can also
`gen.send(True)` to a generator to indicate the children of the current (i.e.
most recently yielded) node do not have to be visited. This obviously only works
in Breath-First, and in Depth-First Pre-order.
"""
from __future__ import annotations

import enum
import typing
import collections

Node = typing.TypeVar('Node')
NOTHING = object()  # Used as `None` without actually being `None`


class Order(enum.Enum):
    BreathFirst = enum.auto()
    DepthFirstPre = enum.auto()
    DepthFirstPost = enum.auto()


class TraverseTree:
    def __init__(self):
        self._nodes_visited = 0

    def __iter__(self) -> TraverseTree:
        return self

    def __next__(self) -> Node:
        self._nodes_visited += 1
        return self.next()

    def next(self) -> Node:
        raise NotImplementedError()

    @property
    def nodes_visited(self) -> int:
        return self._nodes_visited


class TraverseTreeBreathFirst(TraverseTree):
    def __init__(
            self,
            start_node: Node,
            branches: typing.Callable[[Node], typing.Iterable[Node]],
    ):
        super().__init__()
        self.node_queue = collections.deque([start_node])
        self.branches = branches
        self._current_node = NOTHING
        self._descend_into_current_node = True

    def __iter__(self) -> TraverseTree:
        return self

    def next(self) -> Node:
        if self._descend_into_current_node and self._current_node is not NOTHING:
            branches = self.branches(self._current_node)
            self.node_queue.extend(branches)
        try:
            self._descend_into_current_node = True
            self._current_node = self.node_queue.popleft()  # raises IndexError when empty
            return self._current_node
        except IndexError:
            raise StopIteration()

    def dont_descend_into_current_node(self) -> None:
        self._descend_into_current_node = False


class TraverseTreeDepthFirstPre(TraverseTree):
    def __init__(
            self,
            start_node: Node,
            branches: typing.Callable[[Node], typing.Iterable[Node]],
    ):
        super().__init__()
        self.node_queue = collections.deque([start_node])
        self.branches = branches
        self._current_node = NOTHING
        self._descend_into_current_node = True

    def next(self) -> Node:
        if self._descend_into_current_node and self._current_node is not NOTHING:
            branches = list(self.branches(self._current_node))
            self.node_queue.extendleft(reversed(branches))
        try:
            self._descend_into_current_node = True
            self._current_node = self.node_queue.popleft()  # raises IndexError when empty
            return self._current_node
        except IndexError:
            raise StopIteration()

    def dont_descend_into_current_node(self) -> None:
        self._descend_into_current_node = False


class TraverseTreeDepthFirstPost(TraverseTree):
    def __init__(
            self,
            start_node: Node,
            branches: typing.Callable[[Node], typing.Iterable[Node]],
    ):
        super().__init__()
        self.stack: list[tuple[Node, list[Node] | None, int]] = [
            (start_node, list(branches(start_node)), 0)
        ]
        self.branches = branches

    def next(self) -> Node:
        if len(self.stack) == 0:
            raise StopIteration()

        node, branches, branch_nr = self.stack.pop(-1)
        while True:  # until at leaf
            if branch_nr == len(branches):
                return node
                # this level is done, don't push back on stack
            # else:
            self.stack.append((node, branches, branch_nr+1))
            node = branches[branch_nr]
            branches = list(self.branches(node))
            branch_nr = 0


# DEPRECATED FUNCTIONS BELOW


def traverse_breath_first(
        start_node: Node,
        branches: typing.Callable[[Node], typing.Iterable[Node]],
) -> typing.Generator[Node, bool | None, None]:
    it = TraverseTreeBreathFirst(start_node, branches)
    for el in it:
        rx = yield el
        if rx:
            it.dont_descend_into_current_node()


GenType = typing.TypeVar("GenType", bound=typing.Generator)
def for_sendable_generator(gen: GenType) -> GenType:
    """
    Helper to use a generator in a for-loop, and still be able to send to it.
    Normally, it.send() returns the next value, but this makes using a for-loop difficult

    This wrapper will yield the same value twice if non-None is received. This way, it can be used as:

        it = for_sendable_generator(gen())
        for item in it:
            do(item)
            it.send("something")  # this yields the next value, but this wrapper compensates for that
    """
    try:
        rx = None
        while True:  # until StopIteration
            el = gen.send(rx)
            rx = yield el
            if rx is not None:
                yield el
    except StopIteration:
        pass


if __name__ == "__main__":
    import dataclasses
    @dataclasses.dataclass
    class Tree:
        name: str
        branches: list["Tree"]

    tree = Tree(name='root', branches=[
        Tree(name="a", branches=[
            Tree(name="aa", branches=[]),
        ]),
        Tree(name="b", branches=[
            Tree(name="ba", branches=[]),
            Tree(name="bb", branches=[]),
        ]),
        Tree(name="c", branches=[
            Tree(name="ca", branches=[]),
            Tree(name="cb", branches=[
                Tree(name="cba", branches=[]),
                Tree(name="cbb", branches=[]),
            ]),
        ]),
    ])

    # Depth first, pre order
    result = []
    for n in TraverseTreeDepthFirstPre(tree, lambda n: n.branches):
        result.append(n.name)
    assert result == ['root', 'a', 'aa', 'b', 'ba', 'bb', 'c', 'ca', 'cb', 'cba', 'cbb']

    # Depth first, pre order, skip `b`
    result = []
    it = TraverseTreeDepthFirstPre(tree, lambda n: n.branches)
    for n in it:
        result.append(n.name)
        if n.name == 'b':
            it.dont_descend_into_current_node()
    assert result == ['root', 'a', 'aa', 'b', 'c', 'ca', 'cb', 'cba', 'cbb']

    # Depth first, post order
    result = []
    for n in TraverseTreeDepthFirstPost(tree, lambda n: n.branches):
        result.append(n.name)
    assert result == ['aa', 'a', 'ba', 'bb', 'b', 'ca', 'cba', 'cbb', 'cb', 'c', 'root']

    # Breath first
    result = []
    for n in TraverseTreeBreathFirst(tree, lambda n: n.branches):
        result.append(n.name)
    assert result == ['root', 'a', 'b', 'c', 'aa', 'ba', 'bb', 'ca', 'cb', 'cba', 'cbb']

    # Breath first with skip of `b`
    result = []
    it = TraverseTreeBreathFirst(tree, lambda n: n.branches)
    for n in it:
        result.append(n.name)
        if n.name == "b":
            it.dont_descend_into_current_node()
    assert result == ['root', 'a', 'b', 'c', 'aa', 'ca', 'cb', 'cba', 'cbb']

    # legacy below
    # Breath first
    result = []
    for n in traverse_breath_first(tree, lambda n: n.branches):
        result.append(n.name)
    assert result == ['root', 'a', 'b', 'c', 'aa', 'ba', 'bb', 'ca', 'cb', 'cba', 'cbb']

    result = []
    it = for_sendable_generator(traverse_breath_first(tree, lambda n: n.branches))
    for n in it:
        result.append(n.name)
        if n.name == "b":
            it.send(True)
    assert result == ['root', 'a', 'b', 'c', 'aa', 'ca', 'cb', 'cba', 'cbb']

