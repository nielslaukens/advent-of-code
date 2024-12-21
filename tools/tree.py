"""
Tree traversal
"""
from __future__ import annotations

import enum
import typing
import collections
import dataclasses

Node = typing.TypeVar('Node')


class _TraverseTree:
    """
    Base class for tree traversal
    """
    def __init__(self):
        self._nodes_visited = 0

    def __iter__(self) -> _TraverseTree:
        return self

    def __next__(self) -> Node:
        self._nodes_visited += 1
        return self.next()

    def next(self) -> Node:
        raise NotImplementedError()

    @property
    def nodes_visited(self) -> int:
        return self._nodes_visited

    # There is no way to find out how many nodes are still to be visited
    # because branches are only explored on an as-needed basis. We could expose
    # a count of "currently unexplored branches", but that would be a (sometimes
    # huge) under-estimation.
    # Additionally, the branches() callable returns an Iterable, not a (sized)
    # Collection. We could use operator.length_hint() to work around this, but
    # that wouldn't solve the above, bigger, problem.


class _TraverseTree_BreathFirst_or_DepthFirstPre(_TraverseTree):
    """
    Shared logic for both BreathFirst and DepthFirst Pre-order
    """
    def __init__(
            self,
            start_node: Node,
            branches: typing.Callable[[Node], typing.Iterable[Node]],
    ):
        super().__init__()
        self.branches = branches

        # we need a data structure that is efficient to:
        #  - get the first element
        #  - remove the first element
        #  - append (DepthFirst) or prepend (DepthFirstPre) elements
        self.node_queue = collections.deque([
            iter([start_node])
        ])

        self._current_node: Node = None
        self._descend_into_current_node: bool = False  # to bootstrap next()

    def dont_descend_into_current_node(self) -> None:
        self._descend_into_current_node = False

    def _get_next_node(self):
        while True:  # until exception
            try:
                next_iter = self.node_queue[0]  # raises IndexError when node_queue is empty
            except IndexError:
                raise StopIteration()
            try:
                next_node = next(next_iter)  # raises StopIteration when this level is empty
                return next_node
            except StopIteration:
                self.node_queue.popleft()  # will not raise, we got node_queue[0] above

    def next(self) -> Node:
        if self._descend_into_current_node:
            self._extend_node_queue(iter(self.branches(self._current_node)))

        self._current_node = self._get_next_node()  # may raise StopIteration when done
        self._descend_into_current_node = True
        return self._current_node

    def _extend_node_queue(self, branches: typing.Iterator[Node]) -> None:
        raise NotImplementedError("implemented in derived classes")


class TraverseTreeBreathFirst(_TraverseTree_BreathFirst_or_DepthFirstPre):
    """
    Traverse a tree, Breath First.

    Start at node `start_node`. Branches at a given node should be returned by
    the `branches` callable. This expects any iterable, so you can use a list,
    set, generator, ...

    During iteration, you can call TraverseTree.dont_descend_into_current_node()
    to indicate branches below this node do not need to be explored.
    """
    def _extend_node_queue(self, branches: typing.Iterator[Node]) -> None:
        self.node_queue.append(branches)


class TraverseTreeDepthFirstPre(_TraverseTree_BreathFirst_or_DepthFirstPre):
    """
    Traverse a tree, Depth First, pre-order.

    Start at node `start_node`. Branches at a given node should be returned by
    the `branches` callable. This expects any iterable, so you can use a list,
    set, generator, ...

    During iteration, you can call TraverseTree.dont_descend_into_current_node()
    to indicate branches below this node do not need to be explored.
    """
    def _extend_node_queue(self, branches: typing.Iterator[Node]) -> None:
        self.node_queue.appendleft(branches)


class TraverseTreeDepthFirstPost(_TraverseTree):
    """
    Traverse a tree, Depth First, post-order.

    Start at node `start_node`. Branches at a given node should be returned by
    the `branches` callable. This expects any iterable, so you can use a list,
    set, generator, ...

    Since nodes are only returned *after* their children, you can't indicate
    you don't want a subtree explored (cfr breath-first and depth-first
    pre-order)
    """
    @dataclasses.dataclass
    class StackItem:
        node: Node
        remaining_branches: typing.Iterator[Node]

    def __init__(
            self,
            start_node: Node,
            branches: typing.Callable[[Node], typing.Iterable[Node]],
    ):
        super().__init__()
        self.branches = branches

        # we need a data structure that is efficient to:
        #  - get the last element
        #  - remove the last element
        #  - append elements
        self.stack = collections.deque([
            TraverseTreeDepthFirstPost.StackItem(start_node, iter(branches(start_node)))
        ])

    def next(self) -> Node:
        if len(self.stack) == 0:
            raise StopIteration()
        # else:
        # stack[-1] and stack.pop() will not raise, since len() != 0
        #
        # If we pop() in the loop, we return right after, so there is no way
        # we can end up with an empty stack after this point

        while True:
            # examine the top of stack (self.stack[-1])
            try:
                next_branch = next(self.stack[-1].remaining_branches)
            except StopIteration:
                # all branches are done; remove from stack and
                # return the parent node
                stack_item = self.stack.pop()
                return stack_item.node

            # next_branch is the next branch of self.stack[-1].node to explore,
            # descend into it by appending it to the stack and looping around
            self.stack.append(TraverseTreeDepthFirstPost.StackItem(
                next_branch,
                iter(self.branches(next_branch)),
            ))


# DEPRECATED FUNCTIONS BELOW


class Order(enum.Enum):
    BreathFirst = enum.auto()
    DepthFirstPre = enum.auto()
    DepthFirstPost = enum.auto()


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
    import timeit
    import functools

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

    print("testing correctness...")
    # Depth first, pre order
    result = []
    for n in TraverseTreeDepthFirstPre(tree, lambda n: iter(n.branches)):
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
    it = TraverseTreeDepthFirstPost(tree, lambda n: iter(n.branches))
    for n in it:
        result.append(n.name)
        visited = it.nodes_visited
    assert result == ['aa', 'a', 'ba', 'bb', 'b', 'ca', 'cba', 'cbb', 'cb', 'c', 'root']

    # Breath first
    result = []
    for n in TraverseTreeBreathFirst(tree, lambda n: iter(n.branches)):
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

    print("testing performance...")
    def branches(width, depth):
        def _(l):
            if len(l) == depth:
                return []
            for e in range(width):
                yield [*l, e]
        return _
    def test(cls, branches):
        nodes = 0
        for n in cls([], branches):
            nodes += 1
        return nodes
    print("  tree  |  # nodes |   BF  | DFpre | DFpost")
    for name, run_test in [
        ('100w 3d', functools.partial(test, TraverseTreeBreathFirst, branches(100, 3))),
        (' 10w 6d', functools.partial(test, TraverseTreeBreathFirst, branches(10, 6))),
        ('  2w19d', functools.partial(test, TraverseTreeBreathFirst, branches(2, 19))),
    ]:
        print(f"{name}", end='')
        nr_nodes = run_test()
        print(f" | {nr_nodes: 8d}", end='')
        for strategy in [TraverseTreeBreathFirst, TraverseTreeDepthFirstPre, TraverseTreeDepthFirstPost]:
            took = timeit.timeit(run_test, number=3)
            print(f" | {took:.3f}", end='')
        print()

    # legacy below
    # ------------
    # Breath first
    result = []
    for n in traverse_breath_first(tree, lambda n: iter(n.branches)):
        result.append(n.name)
    assert result == ['root', 'a', 'b', 'c', 'aa', 'ba', 'bb', 'ca', 'cb', 'cba', 'cbb']

    result = []
    it = for_sendable_generator(traverse_breath_first(tree, lambda n: iter(n.branches)))
    for n in it:
        result.append(n.name)
        if n.name == "b":
            it.send(True)
    assert result == ['root', 'a', 'b', 'c', 'aa', 'ca', 'cb', 'cba', 'cbb']
