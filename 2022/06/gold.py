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
N = 14
while len(buf) < N or len(set(buf)) != N:
    buf.append(chars.pop(0))
    while len(buf) > N:
        del buf[0]
    i += 1
print(f"{i}: {buf}")
