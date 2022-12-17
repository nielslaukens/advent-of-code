from __future__ import annotations

import enum
import typing


class Node:
    def outbound_edges(self) -> typing.Iterable[Node]:
        raise NotImplementedError()

    class Order(enum.Enum):
        PreOrder = enum.auto()  # emit a node before its children
        PostOrder = enum.auto()  # emit children before the node
        LeafOnly = enum.auto()  # only emit nodes without any children

    def recursive_walk(self, order: Order = Order.PreOrder) -> typing.Generator[Node, None, None]:
        if order == Node.Order.PreOrder:
            yield self

        leaf_node = True
        for node in self.outbound_edges():
            leaf_node = False
            for _ in node.recursive_walk(order):
                yield _

        if order == Node.Order.LeafOnly and leaf_node:
            # _ = list(self.outbound_edges())
            yield self

        if order == Node.Order.PostOrder:
            yield self


if __name__ == "__main__":
    class N(Node):
        def __init__(self, name: str, outb: list = None):
            if outb is None:
                outb = []
            self.name = name
            self.outb = outb

        def outbound_edges(self) -> list[Node]:
            return self.outb

        def __str__(self) -> str:
            return self.name

    aaa = N('aaa')
    aa = N('aa', [aaa])
    ab = N('ab')
    a = N('a', [aa, ab])

    for _ in a.recursive_walk():
        print(_)
