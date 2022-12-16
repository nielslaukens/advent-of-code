import functools

messages: list = []
state = 1
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        if line != "":
            line = eval(line)  # I'm sorry for the eval, I'm too lazy to write a parser
            messages.append(line)

messages.append([[2]])
messages.append([[6]])


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


messages = sorted(messages, key=functools.cmp_to_key(compare))

div1 = None
div2 = None
for i, p in enumerate(messages):
    index = i + 1  # Puzzle uses 1-based indexing
    if p == [[2]]:
        div1 = index
    if p == [[6]]:
        div2 = index

print(div1 * div2)