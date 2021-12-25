import numpy

from tools import numpy_tools

def step_e(seafloor: numpy.ndarray) -> numpy.ndarray:
    new_situation = numpy.full(seafloor.shape, fill_value='.')
    with numpy.nditer(seafloor, flags=['multi_index']) as it:
        for occupant in it:
            if occupant == '.':
                continue
            elif occupant == '>':
                target_location = it.multi_index[0], (it.multi_index[1] + 1) % seafloor.shape[1]
                if seafloor[target_location] == '.':  # move
                    new_situation[target_location] = occupant
                else:  # stay
                    new_situation[it.multi_index[0], it.multi_index[1]] = occupant
            elif occupant == 'v':
                new_situation[it.multi_index[0], it.multi_index[1]] = occupant
    return new_situation


def step_s(seafloor: numpy.ndarray) -> numpy.ndarray:
    new_situation = numpy.full(seafloor.shape, fill_value='.')
    with numpy.nditer(seafloor, flags=['multi_index']) as it:
        for occupant in it:
            if occupant == '.':
                continue
            elif occupant == '>':
                new_situation[it.multi_index[0], it.multi_index[1]] = occupant
            elif occupant == 'v':
                target_location = (it.multi_index[0] + 1) % seafloor.shape[0], it.multi_index[1]
                if seafloor[target_location] == '.':  # move
                    new_situation[target_location] = occupant
                else:  # stay
                    new_situation[it.multi_index[0], it.multi_index[1]] = occupant
    return new_situation


def step(seafloor: numpy.ndarray) -> numpy.ndarray:
    seafloor = step_e(seafloor)
    seafloor = step_s(seafloor)
    return seafloor


with open("25.input.txt", "r") as f:
    lines = []
    for line in f.readlines():
        line = line.strip()
        line = list(line)
        lines.append(line)
    seafloor = numpy.array(lines)

#print(numpy_tools.str_values_only(seafloor))
prev_step = numpy.full(seafloor.shape, fill_value='.')
steps = 0
while (seafloor != prev_step).any():
    prev_step = seafloor
    seafloor = step(seafloor)
    steps += 1
    print(f"\r{steps}")
print(f"stable after {steps} steps:")
print(numpy_tools.str_values_only(seafloor))
