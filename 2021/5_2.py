import re

class SeaFloor:
    """Auto-extending sea floor"""
    def __init__(self):
        self._size = [0, 0]
        self.num_vents = []

    def _extend_y(self, new_max_y):
        if new_max_y < self._size[0]:
            return
        self.num_vents.extend(
            [
                [0 for col in range(0, self._size[1])]
                for row in range(self._size[0], new_max_y+1)
            ]
        )
        self._size[0] = new_max_y+1

    def _extend_x(self, new_max_x):
        if new_max_x < self._size[1]:
            return
        for row in range(0, self._size[0]):
            self.num_vents[row].extend([
                0 for col in range(self._size[1], new_max_x+1)
            ])
        self._size[1] = new_max_x+1

    def _extend(self, new_max_x: int, new_max_y: int):
        self._extend_x(new_max_x)
        self._extend_y(new_max_y)

    def add_vent(self, x: int, y: int):
        self._extend(x, y)
        self.num_vents[y][x] += 1

    def add_vent_line(self, x1, y1, x2, y2):
        if x1 == x2:
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            for y in range(min_y, max_y+1):
                self.add_vent(x1, y)
        elif y1 == y2:
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            for x in range(min_x, max_x+1):
                self.add_vent(x, y1)
        elif abs(y2-y1) == abs(x2-x1):
            # diagonal
            xdir = 1 if x2 > x1 else -1
            ydir = 1 if y2 > y1 else -1
            for i in range(0, abs(x2-x1)+1):
                self.add_vent(
                    x1 + i*xdir,
                    y1 + i*ydir,
                    )
        else:
            raise ValueError(f"({x1},{y1})->({x2},{y2})")

    def __str__(self):
        return '\n'.join([
            ' '.join([str(pos) for pos in row])
            for row in self.num_vents
        ])


vent_lines = []
with open("5_1.input.txt", "r") as f:
    for vent in f.readlines():
        m = re.fullmatch(r'(\d+)\s*,\s*(\d+)\s*->\s*(\d+)\s*,\s*(\d+)\s*', vent)
        vent_lines.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

sea_floor = SeaFloor()
for vent_line in vent_lines:
    sea_floor.add_vent_line(*vent_line)

print(sea_floor)

locations_more_than_two = 0
for row in sea_floor.num_vents:
    for pos in row:
        if pos >= 2:
            locations_more_than_two += 1
print(f"{locations_more_than_two} locations >= 2")