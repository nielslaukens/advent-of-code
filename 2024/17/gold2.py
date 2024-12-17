program = [2,4,1,7,7,5,0,3,4,4,1,7,5,5,3,0]
# 2,4  bst A  B = A % 8
# 1,7  bxl 7  B = B ^ 7
# 7,5  cdv B  C = A // 2**B
# 0,3  adv 3  A = A // 2**3
# 4,4  bxc _  B = B ^ C
# 1,7  bxl 7  B = B ^ 7
# 5,5  out B  output B
# 3,0  jnz 0  loop if A != 0


def my_program_iteration(a: int) -> tuple[int, int, int]:
    b = a % 8  # depends on bit [2:0] of A
    b = b ^ 7  # depends on bit [2:0] of A
    c = a // (2**b)  # need bit [(B+3):B] of A
    a = a // (2**3)  # right shift A by 3
    b = b ^ c  # B[2:0] ^ C[2:0]
    b = b ^ 7  # B[2:0]
    return (a, b, c)

# a[2:0] |  b |     c       | b^c         | ^7          |
# -------+----+-------------+-------------+-------------+
#    000 |  7 | [9] [8] [7] | _9_ _8_ _7_ | [9] [8] [7] |
#    001 |  6 | [8] [7] [6] | _8_ _7_ [6] | [8] [7] _6_ |
#    010 |  5 | [7] [6] [5] | _7_ [6] _5_ | [7] _6_ [5] |
#    011 |  4 | [6] [5] [4] | _6_ [5] [4] | [6] _5_ _4_ |
#    100 |  3 | [5] [4] [3] | [5] _4_ _3_ | _5_ [4] [3] |
#    101 |  2 | [4] [3]  1  | [4] _3_  1  | _4_ [3]  0  |
#    110 |  1 | [3]  1   1  | [3]  1   0  | _3_  0   1  |
#    111 |  0 |  1   1   1  |  1   1   1  |  0   0   0  |


def try_a(a: int):
    out = []
    while a != 0:
        a, b, _ = my_program_iteration(a)
        out.append(b%8)
        if out != program[0:len(out)]:
            return
        if len(out) > len(program):
            return
    if out == program:
        raise RuntimeError(f"found it {a}")


a = 294000000
while True:
    try_a(a)
    a += 1
    if a % 1_000_000 == 0:
        print(f"{a:,}")
