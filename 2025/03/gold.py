import functools

import numpy

battery_banks: list[tuple[str]] = []
with open("input.txt") as f:
    for line in f.readlines():
        bank = tuple(line.rstrip())
        battery_banks.append(bank)

total_joltage = 0

@functools.lru_cache(maxsize=None)
def find_largest_joltage(bank: tuple[str], num: int) -> str:
    # To get the biggest <num> digit number, we need to find the largest digit first
    #  * We need at least <num-1> places left after the selected digit for our second digit
    #  * We may have multiple largest digits, scan them all
    if num == 0:
        return ''

    sorted_indices = list(reversed(numpy.argsort(bank)))
    best_joltage_so_far = None
    for i in sorted_indices:
        # e.g. len(bank) = 3, num==2: i < 1, so we have 2 left for the second digit
        if i > len(bank) - num:
            continue
        if best_joltage_so_far is not None and bank[i] != best_joltage_so_far[0]:
            break
        remaining_digits = find_largest_joltage(tuple(bank[(i+1):]), num-1)
        joltage = bank[i] + remaining_digits
        if best_joltage_so_far is None or joltage > best_joltage_so_far:  # str comparison is fine, same length
            best_joltage_so_far = joltage
    return best_joltage_so_far


for bank in battery_banks:
    j = find_largest_joltage(bank, 12)
    print(f"{''.join(bank)} : {j}")
    total_joltage += int(j)

print(total_joltage)
