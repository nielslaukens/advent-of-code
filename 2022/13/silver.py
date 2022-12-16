message_pairs: list[tuple[list, list]] = []
state = 1
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        if state == 1:
            line1 = eval(line)  # I'm sorry for the eval, I'm too lazy to write a parser
            state = 2
        elif state == 2:
            line2 = eval(line)
            state = 'empty'
        elif state == 'empty':
            message_pairs.append((line1, line2))
            state = 1

    if state == 'empty':
        message_pairs.append((line1, line2))


def compare(left: list | int, right: list | int) -> int:
    """
    Returns 0 if left == right.
    Returns <0 if left < right.
    Returns > 0 if left > right.
    """
    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    assert isinstance(left, list) and isinstance(right, list)
    for i in range(max(len(left), len(right))):
        if i >= len(left):
            return -1  # left < right
        if i >= len(right):
            return 1  # left > right
        c = compare(left[i], right[i])
        if c != 0:
            return c
    return 0


sum_of_correctly_ordered_pairs = 0
for i, p in enumerate(message_pairs):
    index = i + 1  # puzzle is 1-based
    print(f"pair {index}: {p}")
    c = compare(p[0], p[1])
    if c < 0:
        sum_of_correctly_ordered_pairs += index

print(sum_of_correctly_ordered_pairs)
