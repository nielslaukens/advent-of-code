from functools import reduce
import numpy

with open("input.txt") as f:
    cells = [
        row.split()
        for row in f.readlines()
    ]

operations = cells[-1]
numbers = [
    [
        int(value)
        for value in row
    ]
    for row in cells[:-1]
]
numbers = numpy.array(numbers)
print(numbers)
grand_total = 0
for column, operation in enumerate(operations):
    if operation == "+":
        res = reduce(
            lambda acc, e: acc + e,
            numbers[:, column],
            0,
        )
    elif operation == "*":
        res = reduce(
            lambda acc, e: acc * e,
            numbers[:, column],
            1,
        )
    else:
        raise RuntimeError(f"Unknown operation: {operation}")
    grand_total += res

print(grand_total)
