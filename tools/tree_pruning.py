from __future__ import annotations

import math
import numbers

import typing


class Tree:
    def branches(self) -> typing.Iterable[tuple[typing.Any, Tree], None, None]:
        """
        The (sub)branches and leaves at this point in the (sub)tree.

        This method should return pairs of (identifier, subtree_or_leaf)
        """
        raise NotImplementedError()

    def search_best_leaf(
            self, better_than: numbers.Real = -math.inf,
    ) -> tuple[list[typing.Any] | None, numbers.Real | None]:
        """
        Returns the path (a list of identifiers returned by self.branches()) to the leaf
        with the highest score.
        Optionally filter results so only leaves better than `better_than` are considered.
        """
        best_path = None
        best_score = -math.inf
        if self.score_guaranteed_below(better_than):
            return best_path, best_score

        for identifier, branch_or_leaf in self.branches():
            if isinstance(branch_or_leaf, Tree):
                path, score = branch_or_leaf.search_best_leaf(better_than=best_score)
                if path is None:
                    continue
                path.insert(0, identifier)
            elif isinstance(branch_or_leaf, Leaf):
                path = [identifier]
                score = branch_or_leaf.score
            else:
                raise ValueError(f"Unknown type {branch_or_leaf.__class__}")

            if best_path is None or score > best_score:
                best_path = path
                best_score = score

        return best_path, best_score

    def score_guaranteed_below(self, score: numbers.Real) -> bool:
        """
        Pruning condition: can we be sure that this tree has no leaves above score?
        Returning True will prune this (sub)tree from the search.
        """
        return False


class Leaf(Tree):
    def __init__(self, score: numbers.Real):
        self.score = score

    def search_best_leaf(
            self, better_than: numbers.Real = -math.inf
    ) -> tuple[list[typing.Any] | None, numbers.Real | None]:
        return [], self.score


if __name__ == "__main__":
    class TestTree(Tree):
        def __init__(self, branches, guaranteed_max = None):
            self._branches = branches
            self._guaranteed_max = guaranteed_max

        def branches(self) -> typing.Iterable[tuple[typing.Any, Tree | Leaf], None, None]:
            for b in self._branches:
                yield b

        def score_is_below(self, score: numbers.Real) -> bool:
            return self._guaranteed_max is not None and self._guaranteed_max < score


    aa = Leaf(7)
    a = TestTree([('a', aa)])
    ba = Leaf(100)
    b = TestTree([('a', ba)], guaranteed_max=0)  # won't find `ba`
    r = TestTree([('a', a), ('b', b)])

    print(r.search_best_leaf())
