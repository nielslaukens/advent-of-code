with open("input.txt", "r") as f:
    lines = f.readlines()
    assert len(lines) == 1
    stones = [
        int(stone_nr)
        for stone_nr in lines[0].split()
    ]

print(stones)


def blink(stones: list[int]) -> list[int]:
    new_stones: list[int] = []
    for stone_nr in stones:
        if stone_nr == 0:
            new_stones.append(1)
        elif (num_digits := len(digits := str(stone_nr))) % 2 == 0:
            left = digits[0:(num_digits//2)]
            right = digits[(num_digits//2):]
            new_stones.append(int(left))
            new_stones.append(int(right))
        else:
            new_stones.append(stone_nr * 2024)
    return new_stones


for i in range(25):
    stones = blink(stones)
    #print(stones)

print(len(stones))
