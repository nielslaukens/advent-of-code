import numpy

battery_banks: list[list[str]] = []
with open("input.txt") as f:
    for line in f.readlines():
        bank = list(line.rstrip())
        battery_banks.append(bank)

total_joltage = 0

def find_largest_joltage(bank: list[str]) -> int:
    sorted_indices = list(reversed(numpy.argsort(bank)))
    # To get the biggest 2 digit number, we need to find the largest digit first
    #  * We need at least 1 place left after the selected digit for our second digit
    #  * We may have multiple largest digits, scan them all
    best_solution = None
    for i in sorted_indices:
        if best_solution is not None and bank[i] != best_solution['bi']:
            print(f"{''.join(bank)} : {best_solution['i']} {best_solution['j']} {best_solution['num']}")
            return best_solution['num']

        # Find the largest digit on the right of me
        for j in sorted_indices:
            if j > i:
                num = int(f"{bank[i]}{bank[j]}")
                if best_solution is None or num > best_solution['num']:
                    best_solution = {
                        'i': i,
                        'j': j,
                        'bi': bank[i],
                        'bj': bank[j],
                        'num': num,
                    }

    raise RuntimeError("unreachable if len(bank) >= 2")

for bank in battery_banks:
    j = find_largest_joltage(bank)
    total_joltage += j

print(total_joltage)
