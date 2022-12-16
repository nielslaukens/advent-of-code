import dataclasses
import enum
import typing

import numpy as np

from tools.numpy_tools import str_values_only


class Instruction(enum.Enum):
    Noop = "noop"
    Addx = "addx"


x = 1
state_history = [None]  # state at start of cycle N; (cycle 0 does not exist, so None is prepended)
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        words = line.split()
        instr = Instruction(words[0])  # may raise

        if instr == Instruction.Noop:
            state_history.append(x)
        elif instr == Instruction.Addx:
            param = int(words[1])
            state_history.append(x)
            state_history.append(x)
            x += param

    state_history.append(x)

#for cycle, state in enumerate(state_history):
#    print(f"start of {cycle}: {state}")

crt = np.zeros(shape=(6, 40), dtype=int)
for cycle in range(1, len(state_history)):
    row_0 = (cycle-1)//40
    col_0 = ((cycle-1) % 40)
    state_during_cycle = state_history[cycle]

    if state_during_cycle-1 <= col_0 <= state_during_cycle+1:
        crt[row_0, col_0] = 1

print(str_values_only(crt).replace('0', ' ').replace('1', '#'))

