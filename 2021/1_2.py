import typing


class RollingSum:
    def __init__(self, num_samples: int):
        self._num_samples = num_samples
        self._samples = []

    def add(self, data_point: int) -> typing.Optional[int]:
        self._samples.append(data_point)
        while len(self._samples) > self._num_samples:
            self._samples.pop(0)

        if len(self._samples) < self._num_samples:
            return None
        return sum(self._samples)


num_increases = 0
prev_depth = None
r3 = RollingSum(3)
with open("1_1.input.txt", "r") as f:
    for line in f.readlines():
        depth = r3.add(int(line))
        if prev_depth is not None:
            if depth > prev_depth:
                num_increases += 1
        prev_depth = depth

print(num_increases)
