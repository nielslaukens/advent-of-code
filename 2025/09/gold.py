import dataclasses
import time
import typing
from itertools import chain, pairwise

start_time = time.time()

with (open("input.txt") as f):
    red_tile_coords: list[tuple[int, int]] = [
        tuple(int(num) for num in line.split(','))
        for line in f.read().splitlines()
    ]


def edges(vertices: list[tuple[int, int]]) -> typing.Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """
    Returns the edges of the polygon.
    Always returns the lowest vertex first
    """
    for a, b in chain(pairwise(vertices), [(vertices[-1], vertices[0])]):
        yield a, b


@dataclasses.dataclass
class Rect:
    a: tuple[int, int]
    b: tuple[int, int]

    @property
    def area(self) -> int:
        return (abs(self.a[0] - self.b[0])+1) * (abs(self.a[1] - self.b[1])+1)

    def vertices(self):
        return [(self.a[0], self.a[1]), (self.a[0], self.b[1]), (self.b[0], self.b[1]), (self.b[0], self.a[1])]


assert Rect((1, 1), (2,2)).area == 4


def within(side_a: int, num: int, side_b: int, strict: bool = True) -> bool:
    if side_a > side_b:
        side_a, side_b = side_b, side_a
    if strict:
        return side_a < num < side_b
    else:
        return side_a <= num <= side_b


largest_rect = Rect(red_tile_coords[0], red_tile_coords[0])  # bootstrap
for i, a in enumerate(red_tile_coords):
    for j, b in enumerate(red_tile_coords):
        if j <= i:
            continue
        rect = Rect(a, b)
        if rect.area <= largest_rect.area:
            # don't bother checking tiles
            continue

        #print(f"{i}/{len(red_tile_coords)} {j}/{len(red_tile_coords)}")
        fully_inside = True

        # Do a quick check if there are polygon points inside the rectangle
        for p in red_tile_coords:
            if within(a[0], p[0], b[0]) and within(a[1], p[1], b[1]):
                # print(f"{p} inside {a}-{b}")
                fully_inside = False
                break

        # check if there are edges crossing the rectangle
        for edge_a, edge_b in edges(red_tile_coords):
            if edge_a[0] == edge_b[0]:
                dir = 0
            elif edge_a[1] == edge_b[1]:
                dir = 1
            else:
                raise RuntimeError("not horizontal or vertical")
            if within(a[dir], edge_a[dir], b[dir], strict=True) \
                    and within(edge_a[1-dir], a[1-dir], edge_b[1-dir], strict=False):
                fully_inside = False
                break

        if fully_inside and rect.area > largest_rect.area:
            largest_rect = rect

print(largest_rect)
print(largest_rect.area)

print(f"Runtime: {time.time()-start_time:.3f} seconds")
