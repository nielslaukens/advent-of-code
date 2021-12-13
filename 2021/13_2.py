import numpy

from tools.numpy_tools import ndarray_auto_extending_assign, str_highlight_value

dots = []
fold_instructions = []
with open("13.input.txt", "r") as f:
    state = 'dots'
    for line in f.readlines():
        line = line.strip()
        if state == 'dots':
            if line == "":
                state = 'fold_instructions'
            else:
                coords = line.split(',')
                dots.append(tuple([int(_) for _ in coords]))
        elif state == 'fold_instructions':
            line = line[len("fold along "):]
            axis, num = line.split('=')
            fold_instructions.append((axis, int(num)))

sheet = numpy.array([[]], dtype=bool)
for dot in dots:
    sheet = ndarray_auto_extending_assign(sheet, coords=dot, value=True, fill=False)

print(str_highlight_value(sheet.transpose(), 'True'))  # transpose to get Y vertically, and X horizontally


def fold_up(sheet: numpy.ndarray, y: int) -> numpy.ndarray:
    if y != (sheet.shape[1]-1) // 2:
        raise ValueError(f"Can't fold along y={y} with {sheet.shape}")
    top = sheet[:, 0:y]
    bottom = sheet[:, (y+1):]
    bottom_flipped = numpy.flip(bottom, axis=1)
    sheet = top + bottom_flipped
    return sheet


def fold_left(sheet: numpy.ndarray, x: int) -> numpy.ndarray:
    if x != (sheet.shape[0]-1) // 2:
        raise ValueError(f"Can't fold along y={x} with {sheet.shape}")
    left = sheet[0:x, :]
    right = sheet[(x+1):, :]
    right_flipped = numpy.flip(right, axis=0)
    sheet = left + right_flipped
    return sheet


for fold_instruction in fold_instructions:
    print(fold_instruction)
    if fold_instruction[0] == 'x':
        sheet = fold_left(sheet, fold_instruction[1])
    elif fold_instruction[0] == 'y':
        sheet = fold_up(sheet, fold_instruction[1])
    else:
        raise RuntimeError(f"Unrecognized fold: {fold_instruction}")

print(str_highlight_value(
    # transpose to get Y vertically, and X horizontally
    numpy.array2string(sheet.transpose(), max_line_width=300),
    'True'
))
print(numpy.sum(sheet))
