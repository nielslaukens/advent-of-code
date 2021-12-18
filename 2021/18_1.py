import io
import textwrap
import typing


class Pair:
    def __init__(
            self,
            l: typing.Union[int, "Pair"],
            r: typing.Union[int, "Pair"]
    ):
        self.l = l
        self.r = r

    def __repr__(self) -> str:
        return f"[{repr(self.l)},{repr(self.r)}]"

    @classmethod
    def from_str(cls, s: str) -> "Pair":
        stack = []
        for char in s:
            if char in "0123456789":
                char = int(char)
            stack.append(char)
            try:
                if isinstance(stack[-2], int) and isinstance(stack[-1], int):  # join digits together
                    stack[-2:] = [stack[-2] * 10 + stack[-1]]
                if stack[-5] == '[' \
                        and (isinstance(stack[-4], int) or isinstance(stack[-4], Pair)) \
                        and stack[-3] == ',' \
                        and (isinstance(stack[-2], int) or isinstance(stack[-2], Pair)) \
                        and stack[-1] == ']':
                    stack[-5:] = [Pair(stack[-4], stack[-2])]
            except IndexError:
                pass
        assert len(stack) == 1
        assert isinstance(stack[0], Pair)
        return stack[0]

    def pos_iter(self) -> typing.List:
        if isinstance(self.l, int):
            l = [[False]]
        else:
            l = [
                [False] + _
                for _ in self.l.pos_iter()
            ]

        if isinstance(self.r, int):
            r = [[True]]
        else:
            r = [
                [True] + _
                for _ in self.r.pos_iter()
            ]

        return l + r

    def __getitem__(self, pos: typing.List):
        if len(pos) == 0:
            return self

        if pos[0] is False:
            ret = self.l
        else:
            ret = self.r

        if len(pos) > 1:
            ret = ret[pos[1:]]
        return ret

    def __setitem__(self, pos: typing.List, value: typing.Union[int, "Pair"]):
        if len(pos) == 0:
            raise ValueError("Position is empty")
        elif len(pos) == 1:
            if pos[0] is False:
                self.l = value
            else:
                self.r = value
        else:
            if pos[0] is False:
                self.l[pos[1:]] = value
            else:
                self.r[pos[1:]] = value

    def reduce(self):
        while self._reduce_one():
            pass

    def _reduce_one(self):
        # Do we have 4-level-deep pairs?
        positions = self.pos_iter()
        for i in range(len(positions)):
            if len(positions[i]) > 4+1:  # +1, since we count the last number as well
                raise RuntimeError("Should never have nest level > 4")
            elif len(positions[i]) == 4+1:  # explode
                l_num = self[positions[i]]
                r_num = self[positions[i+1]]
                if i > 0:  # there is a number on the left
                    self[positions[i-1]] = self[positions[i-1]] + l_num
                if i+2 < len(positions):  # there is a number to the right
                    self[positions[i+2]] = self[positions[i+2]] + r_num
                self[positions[i][:-1]] = 0
                return True

        # any number > 10?
        for i in range(len(positions)):
            value = self[positions[i]]
            if value >= 10:
                l = value // 2
                r = (value+1) // 2
                self[positions[i]] = Pair(l, r)
                return True

    @property
    def magnitude(self) -> int:
        if isinstance(self.l, int):
            l = self.l
        else:
            l = self.l.magnitude
        if isinstance(self.r, int):
            r = self.r
        else:
            r = self.r.magnitude
        return 3 * l + 2 * r


class SnailFishNumber(Pair):
    def __init__(
            self,
            l: typing.Union[int, "Pair"],
            r: typing.Union[int, "Pair"]
    ):
        super().__init__(l, r)
        self.reduce()

    def __add__(self, other) -> "SnailFishNumber":
        return SnailFishNumber(self, other)

    def __radd__(self, other) -> "SnailFishNumber":
        return SnailFishNumber(other, self)

    @classmethod
    def from_str(cls, s: str) -> "SnailFishNumber":
        p = super().from_str(s)
        return SnailFishNumber(p.l, p.r)


def test_explode_one():
    p = Pair.from_str('[[[[[9,8],1],2],3],4]')
    p._reduce_one()
    assert str(p) == '[[[[0,9],2],3],4]'

    p = Pair.from_str('[7,[6,[5,[4,[3,2]]]]]')
    p._reduce_one()
    assert str(p) == '[7,[6,[5,[7,0]]]]'

    p = Pair.from_str('[[6,[5,[4,[3,2]]]],1]')
    p._reduce_one()
    assert str(p) == '[[6,[5,[7,0]]],3]'

    p = Pair.from_str('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    p._reduce_one()
    assert str(p) == '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'

    p = Pair.from_str('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    p._reduce_one()
    assert str(p) == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'
test_explode_one()


def test_split_one():
    p = Pair.from_str('[11,7]')
    p._reduce_one()
    assert str(p) == '[[5,6],7]'
test_split_one()


def test_reduce():
    p1 = SnailFishNumber.from_str('[[[[4,3],4],4],[7,[[8,4],9]]]')
    p2 = SnailFishNumber.from_str('[1,1]')
    p = p1 + p2
    assert str(p) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
test_reduce()


def sum_lines(data: str) -> SnailFishNumber:
    data = io.StringIO(data)
    terms = [
        SnailFishNumber.from_str(line.strip())
        for line in data.readlines()
    ]
    sum = terms[0]
    for i in range(1, len(terms)):
        sum = sum + terms[i]
    return sum


def test_sum():
    s = sum_lines(textwrap.dedent("""\
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        """))
    assert str(s) == '[[[[1,1],[2,2]],[3,3]],[4,4]]'

    s = sum_lines(textwrap.dedent("""\
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]
        """))
    assert str(s) == '[[[[3,0],[5,3]],[4,4]],[5,5]]'

    s = sum_lines(textwrap.dedent("""\
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]
        [6,6]
        """))
    assert str(s) == '[[[[5,0],[7,4]],[5,5]],[6,6]]'

    s = sum_lines(textwrap.dedent("""\
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
        [7,[5,[[3,8],[1,4]]]]
        [[2,[2,2]],[8,[8,1]]]
        [2,9]
        [1,[[[9,3],9],[[9,0],[0,7]]]]
        [[[5,[7,4]],7],1]
        [[[[4,2],2],6],[8,7]]
        """))
    assert str(s) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
test_sum()


def test_magnitude():
    assert SnailFishNumber.from_str('[9,1]').magnitude == 29
    assert SnailFishNumber.from_str('[1,9]').magnitude == 21
    assert SnailFishNumber.from_str('[[9,1],[1,9]]').magnitude == 129
    assert SnailFishNumber.from_str('[[1,2],[[3,4],5]]').magnitude == 143
    assert SnailFishNumber.from_str('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]').magnitude == 1384
    assert SnailFishNumber.from_str('[[[[1,1],[2,2]],[3,3]],[4,4]]').magnitude == 445
    assert SnailFishNumber.from_str('[[[[3,0],[5,3]],[4,4]],[5,5]]').magnitude == 791
    assert SnailFishNumber.from_str('[[[[5,0],[7,4]],[5,5]],[6,6]]').magnitude == 1137
    assert SnailFishNumber.from_str('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').magnitude == 3488
test_magnitude()

with open("18.input.txt", "r") as f:
    data = f.read()
sum = sum_lines(data)
print(f"sum: {sum}")
print(f"mag: {sum.magnitude}")
