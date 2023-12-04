import dataclasses

import numpy

grid = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        grid.append(list(line))

grid = numpy.array(grid)  # coords: [row_from_top, col_from_left]

it = numpy.nditer(grid, flags=['multi_index'])
symbol_coords = []
for el in it:
    #print(f"{iter.multi_index}: {el}")
    if str(el) not in "0123456789.":  # symbol
        symbol_coords.append(it.multi_index)


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

part_number_sum = 0
for number in numbers:
    is_part_number = False
    for symbol_coord in symbol_coords:
        if number.row-1 <= symbol_coord[0] <= number.row+1 \
                and number.first_char-1 <= symbol_coord[1] <= number.last_char+1:
            is_part_number = True
            break

    print(f"{number} {is_part_number=}")
    if is_part_number:
        part_number_sum += number.value

print(part_number_sum)
# 1510003 too high
