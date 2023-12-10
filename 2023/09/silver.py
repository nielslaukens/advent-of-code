import itertools

sensor_history = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        history = list(map(lambda _: int(_), line.split()))
        sensor_history.append(history)


def derive(values: list[int]) -> list[int]:
    return list(map(lambda _: _[1] - _[0], itertools.pairwise(values)))

result = 0
sensor_values_with_derived = [
    [_] for _ in sensor_history
]
for i in range(len(sensor_history)):
    while not all(map(lambda _: _ == 0, sensor_values_with_derived[i][-1])):
        prev = sensor_values_with_derived[i][-1]
        deriv = derive(prev)
        sensor_values_with_derived[i].append(deriv)

    #print(sensor_values_with_derived[i])

    extrapolate = 0
    for j in range(len(sensor_values_with_derived[i])-2, -1, -1):
        last_j = sensor_values_with_derived[i][j][-1]
        last_j += extrapolate
        extrapolate = last_j
        sensor_values_with_derived[i][j].append(last_j)

    print(sensor_values_with_derived[i][0])
    result += sensor_values_with_derived[i][0][-1]

print(result)
