import typing

with open("input.txt", "r") as f:
    l = f.readlines()
    assert len(l) == 1
    product_ids = l[0].split(',')
    product_ids = [
        tuple(int(_) for _ in p.split('-'))
        for p in product_ids
    ]

def divisors(n: int) -> typing.Generator[int, None, None]:
    for divisor in range(2, n+1):
        if n % divisor == 0:
            yield divisor

def chunk_string(s: str, length: int) -> typing.Generator[str, None, None]:
    for i in range(0, len(s), length):
        yield s[i:i + length]

def is_invalid_n(s: str, n: int) -> bool:
    if len(s) % n != 0:
        return False
    parts = list(chunk_string(s, len(s) // n))
    for part in parts:
        if part != parts[0]:
            return False
    return True

def is_invalid(i: int) -> bool:
    s = str(i)
    for divisor in divisors(len(s)):
        if is_invalid_n(s, divisor):
            return True
    return False

s = 0
for product_range in product_ids:
    for i in range(product_range[0], product_range[1]+1):
        if is_invalid(i):
            print(i)
            s += i

print("sum: ", s)
