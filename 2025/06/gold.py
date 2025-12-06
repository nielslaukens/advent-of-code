from functools import reduce
import numpy

max_length = 0
data = []
with open("input.txt") as f:
    for line in f.readlines():
        line = list(line[:-1])
        max_length = max(max_length, len(line))
        data.append(line)

for row in data:
    while len(row) < max_length:
        row.append(" ")

operators = ''.join(data[-1]).split()
data = data[:-1]
data = numpy.array(data)
data = data.transpose()

def calc(op: str, nums: list[int]) -> int:
    print(op, nums)
    if op == "+":
        return reduce(
            lambda acc, e: acc + e,
            nums,
            0,
        )
    elif op == "*":
        return reduce(
            lambda acc, e: acc * e,
            nums,
            1,
        )
    raise RuntimeError(f"unknown operator: {op}")

grand_total = 0
op = 0
acc = []
for row in data:
    num = ''.join(row)
    if num.strip() == '':
        grand_total += calc(operators[op], acc)
        acc = []
        op += 1
    else:
        acc.append(int(num))

grand_total += calc(operators[op], acc)

print(grand_total)
