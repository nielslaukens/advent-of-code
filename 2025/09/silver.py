import dataclasses

with (open("input.txt") as f):
    red_tile_coords: list[tuple[int, int]] = [
        [int(num) for num in line.split(',')]
        for line in f.read().splitlines()
    ]


@dataclasses.dataclass
class Rect:
    a: tuple[int, int]
    b: tuple[int, int]

    @property
    def area(self) -> int:
        return (abs(self.a[0] - self.b[0])+1) * (abs(self.a[1] - self.b[1])+1)


assert Rect((1, 1), (2,2)).area == 4


largest_rect = Rect(red_tile_coords[0], red_tile_coords[0])  # bootstrap
for i, a in enumerate(red_tile_coords):
    for j, b in enumerate(red_tile_coords):
        if j <= i:
            continue
        rect = Rect(a, b)
        if rect.area > largest_rect.area:
            largest_rect = rect

print(largest_rect)
print(largest_rect.area)
