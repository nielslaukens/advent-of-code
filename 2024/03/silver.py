import re

with open("input.txt", "r") as f:
    memory = ''.join(f.readlines())

total = 0
for instruction in re.finditer(r'mul\((?P<f1>\d{1,3}),(?P<f2>\d{1,3})\)', memory):
    product = int(instruction.group('f1')) * int(instruction.group('f2'))
    print(instruction, " => ", product)
    total += product

print(total)
