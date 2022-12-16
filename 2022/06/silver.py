with open("input.txt", 'r') as f:
    lines = [
        _.rstrip()
        for _ in f
    ]
assert len(lines) == 1
chars = list(lines[0])
print(chars)

i = 0
buf = []
while len(buf) < 4 or len(set(buf)) != 4:
    buf.append(chars.pop(0))
    while len(buf) > 4:
        del buf[0]
    i += 1
print(f"{i}: {buf}")
