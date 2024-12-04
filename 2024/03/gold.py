import re

with open("input.txt", "r") as f:
    memory = ''.join(f.readlines())

total = 0
enabled = True
for instruction in re.finditer(r'((?P<mul>mul)\((?P<f1>\d{1,3}),(?P<f2>\d{1,3})\))|((?P<endis>(do|don\'t))\(\))', memory):
    endis = instruction.group('endis')
    if endis is not None:
        if endis == "don't":
            enabled = False
        elif endis == "do":
            enabled = True
        else:
            raise RuntimeError("Unreachable")
        continue

    product = int(instruction.group('f1')) * int(instruction.group('f2'))
    print(instruction, " => ", product, enabled)
    if enabled:
        total += product

print(total)
