from __future__ import annotations

import dataclasses
import itertools
import typing

import numpy as np


@dataclasses.dataclass
class LockKey:
    pins: np.ndarray

    @staticmethod
    def parse(block: list[str]) -> LockKey:
        if block[0] == "#####":
            cls = Lock
        elif block[-1] == "#####":
            cls = Key
            block = list(reversed(block))
        else:
            raise ValueError()
        block = np.array([list(row) for row in block])
        pins = []
        for col in range(block.shape[1]):
            pin = block[:, col]
            assert pin[0] == "#"
            pin_length = int(sum(pin == '#')) - 1
            pins.append(pin_length)
        return cls(np.array(pins))


class Lock(LockKey):
    pass


class Key(LockKey):
    pass


locks: list[Lock] = []
keys: list[Key] = []
def add(block: list[str]):
    lk = Lock.parse(block)
    if isinstance(lk, Lock):
        locks.append(lk)
    elif isinstance(lk, Key):
        keys.append(lk)
    else:
        RuntimeError()


with open("input.txt", "r") as f:
    block = []
    for line in f:
        line = line.strip()
        if line == "":
            add(block)
            block = []
            continue
        block.append(line)
    add(block)

print(locks)
print(keys)

fit = 0
for lock, key in itertools.product(locks, keys):
    overlap = lock.pins + key.pins
    pins_overlap = np.any(overlap > 5)
    print(lock, key, pins_overlap)
    if not pins_overlap:
        fit += 1

print(fit)
