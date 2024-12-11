import functools

with open("input.txt", "r") as f:
    lines = f.readlines()
    assert len(lines) == 1
    stones = [
        int(stone_nr)
        for stone_nr in lines[0].split()
    ]

print(stones)


# Stones never merge, so we can iterate blinks per stone
# Also, since all stones follow the same pattern, we can cache results
@functools.lru_cache(maxsize=1024*1024)
def number_of_stones_after_blinks(stone_nr: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone_nr == 0:
        return number_of_stones_after_blinks(1, blinks - 1)
    elif (num_digits := len(digits := str(stone_nr))) % 2 == 0:
        left = int(digits[0:(num_digits//2)])
        right = int(digits[(num_digits//2):])
        left_stones = number_of_stones_after_blinks(left, blinks - 1)
        right_stones = number_of_stones_after_blinks(right, blinks - 1)
        return left_stones + right_stones
    else:
        return number_of_stones_after_blinks(stone_nr * 2024, blinks - 1)


NUM_BLINKS = 75
total_number_of_stones = 0
for i, stone_nr in enumerate(stones):
    total_number_of_stones += number_of_stones_after_blinks(stone_nr, NUM_BLINKS)

print(f"{total_number_of_stones=}")
