"""
Tree traversal Generators.

You can optionally send(True) to a generator to indicate the children of this
node do not have to be visited. This obviously only works in Breath-First, and
in Depth-First Pre-order.
"""
import enum
import typing

Node = typing.TypeVar('Node')


class Order(enum.Enum):
    Pre = enum.auto()
    Post = enum.auto()
    LeafOnly = enum.auto()  # Only yield nodes without branches


def traverse_depth_first(
        start_node: Node,
        branches: typing.Callable[[Node], typing.Iterable[Node]],
        order: Order = Order.Pre,
) -> typing.Generator[Node, bool | None, None]:
    skip = False
    if order == Order.Pre:
        skip = yield start_node

    leaf = True
    if not skip:
        for branch in branches(start_node):
            yield from traverse_depth_first(branch, branches, order)
            leaf = False

    if leaf and order == Order.LeafOnly:
        yield start_node

    if order == Order.Post:
        yield start_node


def traverse_breath_first(
        start_node: Node,
        branches: typing.Callable[[Node], typing.Iterable[Node]],
) -> typing.Generator[Node, bool | None, None]:
    subbranches = [start_node]
    while len(subbranches) > 0:
        node = subbranches.pop(0)
        skip = yield node
        if not skip:
            subbranches.extend(branches(node))


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

    print("Depth first:")
    for n in traverse_depth_first(
            tree,
            lambda n: n.branches,
            Order.LeafOnly,
    ):
        print(n.name)

    print("Breath first:")
    for n in traverse_breath_first(
            tree,
            lambda n: n.branches,
    ):
        print(n.name)

    print("Depth first with skip of `b`:")
    it = for_sendable_generator(traverse_depth_first(tree, lambda n: n.branches, Order.Pre))
    for n in it:
        print(n.name)
        if n.name == "b":
            it.send(True)

    print("Breath first with skip of `b`:")
    it = for_sendable_generator(traverse_breath_first(tree, lambda n: n.branches))
    for n in it:
        print(n.name)
        if n.name == "b":
            it.send(True)
