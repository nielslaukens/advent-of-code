import dataclasses
import enum
import typing


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

total_signal_strength = 0
for cycle in [20, 60, 100, 140, 180, 220]:
    ss = cycle * state_history[cycle]
    print(f"state during {cycle}: state={state_history[cycle]}, signal strength = {ss}")
    total_signal_strength += ss

print(total_signal_strength)
