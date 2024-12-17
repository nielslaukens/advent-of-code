program = [2,4,1,7,7,5,0,3,4,4,1,7,5,5,3,0]
# 2,4  bst A  B = A % 8
# 1,7  bxl 7  B = B ^ 7
# 7,5  cdv B  C = A // 2**B
# 0,3  adv 3  A = A // 2**3
# 4,4  bxc _  B = B ^ C
# 1,7  bxl 7  B = B ^ 7
# 5,5  out B  output B
# 3,0  jnz 0  loop if A != 0
def my_program_iteration(a: int) -> tuple[int, int]:
    b = a % 8  # depends on bit [2:0] of A
    b = b ^ 7  # depends on bit [2:0] of A
    c = a // (2**b)  # need bit [(B+3):B] of A
    a = a // (2**3)  # right shift A by 3
    b = b ^ c  # B[2:0] ^ C[2:0]
    b = b ^ 7  # B[2:0]
    return (a, b%8)

# a[2:0] |  b |     c       | b^c         | ^7, output  |
# -------+----+-------------+-------------+-------------+
#    000 |  7 | [9] [8] [7] | _9_ _8_ _7_ | [9] [8] [7] |
#    001 |  6 | [8] [7] [6] | _8_ _7_ [6] | [8] [7] _6_ |
#    010 |  5 | [7] [6] [5] | _7_ [6] _5_ | [7] _6_ [5] |
#    011 |  4 | [6] [5] [4] | _6_ [5] [4] | [6] _5_ _4_ |
#    100 |  3 | [5] [4] [3] | [5] _4_ _3_ | _5_ [4] [3] |
#    101 |  2 | [4] [3]  1  | [4] _3_  1  | _4_ [3]  0  |
#    110 |  1 | [3]  1   1  | [3]  1   0  | _3_  0   1  |
#    111 |  0 |  1   1   1  |  1   1   1  |  0   0   0  |

def three_bits(i: int) -> list[str]:
    i = bin(i)[2:]
    return list(('00' + i)[-3:])

def options_for_output(b: int):
    assert 0 <= b < 8
    opts = {}
    for a20 in range(8):
        o = list('xxxxxxxxxx')
        o[7:10] = three_bits(a20)
        output_bits = three_bits(b ^ a20)
        for i in range(3):
            if o[a20+i] == 'x':
                o[a20+i] = output_bits[i]
            elif o[a20+i] == output_bits[i]:
                pass
            else:  # not 'x' and not same
                continue
        while o[0] == 'x':
            o = o[1:]
        opts[a20] = list(reversed(o))
    if b != 0:
        try:
            del opts[0b111]
        except KeyError:
            pass
    if b % 4 != 0b01:
        try:
            del opts[0b110]
        except KeyError:
            pass
    if b % 2 != 0b0:
        try:
            del opts[0b101]
        except KeyError:
            pass
    return opts.values()


for opt in options_for_output(2):
    print(opt)
