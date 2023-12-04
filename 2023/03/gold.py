import dataclasses

import numpy

grid = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        grid.append(list(line))

grid = numpy.array(grid)  # coords: [row_from_top, col_from_left]

it = numpy.nditer(grid, flags=['multi_index'])
gear_coords = []
for el in it:
    #print(f"{iter.multi_index}: {el}")
    if str(el) == "*":  # gear
        gear_coords.append(it.multi_index)


@dataclasses.dataclass
class Number:
    value: int
    row: int
    first_char: int
    last_char: int

    @classmethod
    def factory(cls, value: str, row: int, last_char: int):
        first_char = last_char - len(value) + 1
        return cls(value=int(value), row=row, first_char=first_char, last_char=last_char)

    def touching(self, row: int, col: int) -> bool:
        return self.row-1 <= row <= self.row+1 \
            and self.first_char-1 <= col <= self.last_char+1


numbers: list[Number] = []
prev_chars = ''
last_coord = None
for row in range(grid.shape[0]):
    for col in range(grid.shape[1]):
        ch = str(grid[row, col])
        if ch in "0123456789":
            prev_chars += ch
            last_coord = (row, col)
        elif prev_chars != '':
            numbers.append(Number.factory(prev_chars, row=last_coord[0], last_char=last_coord[1]))
            #print(f"{row}, {col}: {prev_chars}")
            prev_chars = ''
            last_coord = None
    if prev_chars != '':
        numbers.append(Number.factory(prev_chars, row=last_coord[0], last_char=last_coord[1]))
        prev_chars = ''
        last_coord = None

gear_ratio_sum = 0
for gear_coord in gear_coords:
    touching_numbers = []
    for number in numbers:
        if number.touching(gear_coord[0], gear_coord[1]):
            touching_numbers.append(number)

    if len(touching_numbers) == 2:
        gear_ratio = touching_numbers[0].value * touching_numbers[1].value
        print(f"gear at {gear_coord}: {gear_ratio} {touching_numbers}")
        gear_ratio_sum += gear_ratio

print(gear_ratio_sum)
