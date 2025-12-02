with open("input.txt", "r") as f:
    l = f.readlines()
    assert len(l) == 1
    product_ids = l[0].split(',')
    product_ids = [
        tuple(int(_) for _ in p.split('-'))
        for p in product_ids
    ]

def is_invalid(i: int) -> bool:
    s = str(i)
    if len(s) % 2 == 1:
        # can't consist of 2 repetitions if it isn't even length
        return False
    first_half = s[:len(s) // 2]
    last_half = s[len(s) // 2:]
    return first_half == last_half

s = 0
for product_range in product_ids:
    for i in range(product_range[0], product_range[1]+1):
        if is_invalid(i):
            s += i

print(s)
