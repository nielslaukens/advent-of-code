"""
Hand-translated and optimized
"""
import typing


def run0(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1
    # add x 14
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 7
    # mul y x
    # add z y
    return z + inp + 7

def run1(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1
    # add x 12
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 4
    # mul y x
    # add z y
    return 26 * z + (inp + 4)

def run2(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1
    # add x 11
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 8
    # mul y x
    # add z y
    return 26 * z + (inp + 8)

def run3(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 26
    # add x -4
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 1
    # mul y x
    # add z y
    w = inp
    z, x = divmod(z, 26)
    if x - 4 != w:
        z = 26 * z + (w + 1)
    return z

def run4(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1
    # add x 10
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 5
    # mul y x
    # add z y
    return 26 * z + (inp + 5)

def run5(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1
    # add x 10
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 14
    # mul y x
    # add z y
    return 26 * z + (inp + 14)

def run6(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1
    # add x 15
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 12
    # mul y x
    # add z y
    return 26 * z + (inp + 12)

def run7(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 26
    # add x -9
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 10
    # mul y x
    # add z y
    w = inp
    z, x = divmod(z, 26)
    if x - 9 != w:
        z = 26 * z + (w + 10)
    return z

def run8(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 26
    # add x -9
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 5
    # mul y x
    # add z y
    w = inp
    z, x = divmod(z, 26)
    if x - 9 != w:
        z = 26 * z + (w + 5)
    return z

def run9(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1
    # add x 12
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 7
    # mul y x
    # add z y
    return 26 * z + (inp + 7)

def run10(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 26
    # add x -15
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 6
    # mul y x
    # add z y
    w = inp
    z, x = divmod(z, 26)
    if x - 15 != w:
        z = 26 * z + (w + 6)
    return z

def run11(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 26
    # add x -7
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 8
    # mul y x
    # add z y
    w = inp
    z, x = divmod(z, 26)
    if x - 7 != w:
        z = 26 * z + (w + 8)
    return z

def run12(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 26
    # add x -10
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 4
    # mul y x
    # add z y
    w = inp
    z, x = divmod(z, 26)
    if x - 10 != w:
        z = 26 * z + (w + 4)
    return z

def run13(z: int, inp: int) -> int:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 26
    # add x 0
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 6
    # mul y x
    # add z y
    w = inp
    z, x = divmod(z, 26)
    if x + 0 != w:
        z = 26 * z + (w + 6)
    return z



steps = [run0, run1, run2, run3, run4, run5, run6, run7, run8, run9, run10, run11, run12, run13]


def run_all(inp: typing.List[int]) -> int:
    z = 0
    for i, run in enumerate(steps):
        z = run(z, inp[i])
    return z


def run(inp: typing.List[int]) -> int:
    # 3a, 7b, 8b, 10b, 11b, 12b, 13b => not possible
    # 3b, 7a, 8b, 10b, 11b, 12b, 13b => not possible
    # 3b, 7b, 8a, 10b, 11b, 12b, 13b => not possible
    # 3b, 7b, 8b, 10a, 11b, 12b, 13b => not possible
    # 3b, 7b, 8b, 10b, 11a, 12b, 13b => not possible
    # 3b, 7b, 8b, 10b, 11b, 12a, 13b => not possible
    # 3b, 7b, 8b, 10b, 11b, 12b, 13b => z < inp[0] < 3
    z = inp[0] + 7

    # 3a, 7b, 8b, 10b, 11b, 12b, 13b => z == 0 && inp[1] < 6
    # 3b, 7a, 8a, 10b, 11b, 12b, 13b => not possible
    # 3b, 7a, 8b, 10a, 11b, 12b, 13b => not possible
    # 3b, 7a, 8b, 10b, 11a, 12b, 13b => not possible
    # 3b, 7a, 8b, 10b, 11b, 12a, 13b => not possible
    # 3b, 7a, 8b, 10b, 11b, 12b, 13b => z == 0 && inp[1] < 6
    # 3b, 7b, 8a, 10a, 11b, 12b, 13b => not possible
    # 3b, 7b, 8a, 10b, 11a, 12b, 13b => not possible
    # 3b, 7b, 8a, 10b, 11b, 12a, 13b => not possible
    # 3b, 7b, 8a, 10b, 11b, 12b, 13b => z == 0 && inp[1] < 6
    # 3b, 7b, 8b, 10a, 11a, 12b, 13b => not possible
    # 3b, 7b, 8b, 10a, 11b, 12a, 13b => not possible
    # 3b, 7b, 8b, 10a, 11b, 12b, 13b => z == 0 && inp[1] < 6
    # 3b, 7b, 8b, 10b, 11a, 12b, 13b => z == 0 && inp[1] < 6
    # 3b, 7b, 8b, 10b, 11b, 12a, 13b => z == 0
    # 3b, 7b, 8b, 10b, 11b, 12b, 13b => z < 10
    z = 26 * z + (inp[1] + 4)

    # 3a, 7a, 8b, 10b, 11b, 12b, 13b => not possible
    # 3a, 7b, 8a, 10b, 11b, 12b, 13b => not possible
    # 3a, 7b, 8b, 10a, 11b, 12b, 13b => not possible
    # 3a, 7b, 8b, 10b, 11a, 12b, 13b => not possible
    # 3a, 7b, 8b, 10b, 11b, 12a, 13b => not possible
    # 3a, 7b, 8b, 10b, 11b, 12b, 13b => z < 10
    # 3b, 7a, 8a, 10b, 11b, 12b, 13b => z == 0
    # 3b, 7a, 8b, 10a, 11b, 12b, 13b => z == 0
    # 3b, 7a, 8b, 10b, 11a, 12b, 13b => z == 0
    # 3b, 7a, 8b, 10b, 11b, 12a, 13b => z == 0
    # 3b, 7a, 8b, 10b, 11b, 12b, 13b => z < 10
    # 3b, 7b, 8a, 10a, 11b, 12b, 13b => z == 0
    # 3b, 7b, 8a, 10b, 11a, 12b, 13b => z == 0
    # 3b, 7b, 8a, 10b, 11b, 12a, 13b => z == 0
    # 3b, 7b, 8a, 10b, 11b, 12b, 13b => z < 10
    # 3b, 7b, 8b, 10a, 11a, 12b, 13b => z == 0
    # 3b, 7b, 8b, 10a, 11b, 12a, 13b => z == 0
    # 3b, 7b, 8b, 10a, 11b, 12b, 13b => z < 10
    # 3b, 7b, 8b, 10b, 11a, 12b, 13b => z < 10
    # 3b, 7b, 8b, 10b, 11b, 12a, 13b => z < 20
    # 3b, 7b, 8b, 10b, 11b, 12b, 13b => z < 260
    z = 26 * z + (inp[2] + 8)

    # 3a: inp[3] != z % 26 - 4
    # 3b: inp[3] == z % 26 - 4
    # 3a, 7a, 8a, 10b, 11b, 12b, 13b => not possible
    # 3a, 7a, 8b, 10a, 11b, 12b, 13b => not possible
    # 3a, 7a, 8b, 10b, 11a, 12b, 13b => not possible
    # 3a, 7a, 8b, 10b, 11b, 12a, 13b => not possible
    # 3a, 7a, 8b, 10b, 11b, 12b, 13b => z == 0 && inp[3] < 9
    # 3a, 7b, 8a, 10a, 11b, 12b, 13b => not possible
    # 3a, 7b, 8a, 10b, 11a, 12b, 13b => not possible
    # 3a, 7b, 8a, 10b, 11b, 12a, 13b => not possible
    # 3a, 7b, 8a, 10b, 11b, 12b, 13b => z == 0 && inp[3] < 9
    # 3a, 7b, 8b, 10a, 11a, 12b, 13b => not possible
    # 3a, 7b, 8b, 10a, 11b, 12a, 13b => not possible
    # 3a, 7b, 8b, 10a, 11b, 12b, 13b => z == 0 && inp[3] < 9
    # 3a, 7b, 8b, 10b, 11a, 12b, 13b => z == 0 && inp[3] < 9
    # 3a, 7b, 8b, 10b, 11b, 12a, 13b => z == 0
    # 3a, 7b, 8b, 10b, 11b, 12b, 13b => z < 260
    # 3b, 7a, 8a, 10b, 11b, 12b, 13b => z < 26
    # 3b, 7a, 8b, 10a, 11b, 12b, 13b => z < 26
    # 3b, 7a, 8b, 10b, 11a, 12b, 13b => z < 26
    # 3b, 7a, 8b, 10b, 11b, 12a, 13b => z < 26
    # 3b, 7a, 8b, 10b, 11b, 12b, 13b => z < 260
    # 3b, 7b, 8a, 10a, 11b, 12b, 13b => z < 26
    # 3b, 7b, 8a, 10b, 11a, 12b, 13b => z < 26
    # 3b, 7b, 8a, 10b, 11b, 12a, 13b => z < 26
    # 3b, 7b, 8a, 10b, 11b, 12b, 13b => z < 260
    # 3b, 7b, 8b, 10a, 11a, 12b, 13b => z < 26
    # 3b, 7b, 8b, 10a, 11b, 12a, 13b => z < 26
    # 3b, 7b, 8b, 10a, 11b, 12b, 13b => z < 260
    # 3b, 7b, 8b, 10b, 11a, 12b, 13b => z < 260
    # 3b, 7b, 8b, 10b, 11b, 12a, 13b => z < 520
    # 3b, 7b, 8b, 10b, 11b, 12b, 13b => z < 6760
    w = inp[3]
    z, x = divmod(z, 26)
    if x - 4 != w:
        z = 26 * z + (w + 1)
        raise ValueError(f"3: {x - 4} != {w}")

    # 7a, 8a, 10b, 11b, 12a, 13b => not possible
    # 7a, 8a, 10b, 11b, 12b, 13b => z == 0 && inp[4] < 5
    # 7a, 8b, 10a, 11b, 12a, 13b => not possible
    # 7a, 8b, 10a, 11b, 12b, 13b => z == 0 && inp[4] < 5
    # 7a, 8b, 10b, 11a, 12b, 13b => z == 0 && inp[4] < 5
    # 7a, 8b, 10b, 11b, 12a, 13b => z == 0
    # 7a, 8b, 10b, 11b, 12b, 13b => z < 10
    # 7b, 8a, 10a, 11a, 12b, 13b => not possible
    # 7b, 8a, 10a, 11b, 12a, 13b => not possible
    # 7b, 8a, 10a, 11b, 12b, 13b => z == 0 && inp[4] < 5
    # 7b, 8a, 10b, 11a, 12b, 13b => z == 0 && inp[4] < 5
    # 7b, 8a, 10b, 11b, 12a, 13b => z == 0
    # 7b, 8a, 10b, 11b, 12b, 13b => z < 10
    # 7b, 8b, 10a, 11a, 12b, 13b => z == 0 && inp[4] < 5
    # 7b, 8b, 10a, 11b, 12a, 13b => z == 0
    # 7b, 8b, 10a, 11b, 12b, 13b => z < 10
    # 7b, 8b, 10b, 11a, 12a, 13b => not possible
    # 7b, 8b, 10b, 11a, 12b, 13b => z < 10
    # 7b, 8b, 10b, 11b, 12a, 13b => z < 20
    # 7b, 8b, 10b, 11b, 12b, 13b => z < 260
    z = 26 * z + (inp[4] + 5)

    # 7a, 8a, 10a, 11a, 12b, 13b => not possible
    # 7a, 8a, 10a, 11b, 12a, 13b => not possible
    # 7a, 8a, 10a, 11b, 12b, 13b => not possible
    # 7a, 8a, 10b, 11a, 12b, 13b => not possible
    # 7a, 8a, 10b, 11b, 12a, 13b => z == 0 && inp[5] < 6
    # 7a, 8a, 10b, 11b, 12b, 13b => z < 10
    # 7a, 8b, 10a, 11a, 12b, 13b => not possible
    # 7a, 8b, 10a, 11b, 12a, 13b => z == 0 && inp[5] < 6
    # 7a, 8b, 10a, 11b, 12b, 13b => z < 10
    # 7a, 8b, 10b, 11a, 12a, 13b => not possible
    # 7a, 8b, 10b, 11a, 12b, 13b => z < 10
    # 7a, 8b, 10b, 11b, 12a, 13b => z < 20
    # 7a, 8b, 10b, 11b, 12b, 13b => z < 260
    # 7b, 8a, 10a, 11a, 12b, 13b => z == 0
    # 7b, 8a, 10a, 11b, 12a, 13b => z == 0
    # 7b, 8a, 10a, 11b, 12b, 13b => z < 10
    # 7b, 8a, 10b, 11a, 12b, 13b => z < 10
    # 7b, 8a, 10b, 11b, 12a, 13b => z < 20
    # 7b, 8a, 10b, 11b, 12b, 13b => z < 260
    # 7b, 8b, 10a, 11a, 12b, 13b => z < 10
    # 7b, 8b, 10a, 11b, 12a, 13b => z < 20
    # 7b, 8b, 10a, 11b, 12b, 13b => z < 260
    # 7b, 8b, 10b, 11a, 12a, 13b => z == 0
    # 7b, 8b, 10b, 11a, 12b, 13b => z < 260
    # 7b, 8b, 10b, 11b, 12a, 13b => z < 520
    # 7b, 8b, 10b, 11b, 12b, 13b => z < 6760
    z = 26 * z + (inp[5] + 14)

    # 7a, 8a, 10a, 11a, 12b, 13b => z == 0
    # 7a, 8a, 10a, 11b, 12a, 13b => z == 0
    # 7a, 8a, 10a, 11b, 12b, 13b => z < 10
    # 7a, 8a, 10b, 11a, 12b, 13b => z < 10
    # 7a, 8a, 10b, 11b, 12a, 13b => z < 20
    # 7a, 8a, 10b, 11b, 12b, 13b => z < 260
    # 7a, 8b, 10a, 11a, 12b, 13b => z < 10
    # 7a, 8b, 10a, 11b, 12a, 13b => z < 20
    # 7a, 8b, 10a, 11b, 12b, 13b => z < 260
    # 7a, 8b, 10b, 11a, 12a, 13b => z == 0
    # 7a, 8b, 10b, 11a, 12b, 13b => z < 260
    # 7a, 8b, 10b, 11b, 12a, 13b => z < 520
    # 7a, 8b, 10b, 11b, 12b, 13b => z < 6760
    # 7b, 8a, 10a, 11a, 12b, 13b => z < 26
    # 7b, 8a, 10a, 11b, 12a, 13b => z < 26
    # 7b, 8a, 10a, 11b, 12b, 13b => z < 260
    # 7b, 8a, 10b, 11a, 12b, 13b => z < 260
    # 7b, 8a, 10b, 11b, 12a, 13b => z < 520
    # 7b, 8a, 10b, 11b, 12b, 13b => z < 6760
    # 7b, 8b, 10a, 11a, 12b, 13b => z < 260
    # 7b, 8b, 10a, 11b, 12a, 13b => z < 520
    # 7b, 8b, 10a, 11b, 12b, 13b => z < 6760
    # 7b, 8b, 10b, 11a, 12a, 13b => z < 26
    # 7b, 8b, 10b, 11a, 12b, 13b => z < 6760
    # 7b, 8b, 10b, 11b, 12a, 13b => z < 13520
    # 7b, 8b, 10b, 11b, 12b, 13b => z < 175760
    z = 26 * z + (inp[6] + 12)

    # 7a: inp[7] != z % 26 - 9
    # 7b: inp[7] == z % 26 - 9
    # 7a, 8a, 10a, 11a, 12b, 13b => z < 26
    # 7a, 8a, 10a, 11b, 12a, 13b => z < 26
    # 7a, 8a, 10a, 11b, 12b, 13b => z < 260
    # 7a, 8a, 10b, 11a, 12b, 13b => z < 260
    # 7a, 8a, 10b, 11b, 12a, 13b => z < 520
    # 7a, 8a, 10b, 11b, 12b, 13b => z < 6760
    # 7a, 8b, 10a, 11a, 12b, 13b => z < 260
    # 7a, 8b, 10a, 11b, 12a, 13b => z < 520
    # 7a, 8b, 10a, 11b, 12b, 13b => z < 6760
    # 7a, 8b, 10b, 11a, 12a, 13b => z < 26
    # 7a, 8b, 10b, 11a, 12b, 13b => z < 6760
    # 7a, 8b, 10b, 11b, 12a, 13b => z < 13520
    # 7a, 8b, 10b, 11b, 12b, 13b => z < 175760
    # 7b, 8a, 10a, 11a, 12b, 13b => z < 676
    # 7b, 8a, 10a, 11b, 12a, 13b => z < 676
    # 7b, 8a, 10a, 11b, 12b, 13b => z < 6760
    # 7b, 8a, 10b, 11a, 12b, 13b => z < 6760
    # 7b, 8a, 10b, 11b, 12a, 13b => z < 13520
    # 7b, 8a, 10b, 11b, 12b, 13b => z < 175760
    # 7b, 8b, 10a, 11a, 12b, 13b => z < 6760
    # 7b, 8b, 10a, 11b, 12a, 13b => z < 13520
    # 7b, 8b, 10a, 11b, 12b, 13b => z < 175760
    # 7b, 8b, 10b, 11a, 12a, 13b => z < 676
    # 7b, 8b, 10b, 11a, 12b, 13b => z < 175760
    # 7b, 8b, 10b, 11b, 12a, 13b => z < 351520
    # 7b, 8b, 10b, 11b, 12b, 13b => z < 4569760
    w = inp[7]
    z, x = divmod(z, 26)
    if x - 9 != w:
        z = 26 * z + (w + 10)
        raise ValueError(f"7: {x - 9} != {w}")

    # 8a: inp[8] != z % 26 - 9
    # 8b: inp[8] == z % 26 - 9
    # 8a, 10a, 11a, 12b, 13b => z < 26 && inp[8] < 5
    # 8a, 10a, 11b, 12a, 13b => z < 26
    # 8a, 10a, 11b, 12b, 13b => z < 260
    # 8a, 10b, 11a, 12a, 13b => not possible
    # 8a, 10b, 11a, 12b, 13b => z < 260
    # 8a, 10b, 11b, 12a, 13b => z < 520
    # 8a, 10b, 11b, 12b, 13b => z < 6760
    # 8b, 10a, 11a, 12b, 13b => z < 260
    # 8b, 10a, 11b, 12a, 13b => z < 520
    # 8b, 10a, 11b, 12b, 13b => z < 6760
    # 8b, 10b, 11a, 12a, 13b => z < 26
    # 8b, 10b, 11a, 12b, 13b => z < 6760
    # 8b, 10b, 11b, 12a, 13b => z < 13520
    # 8b, 10b, 11b, 12b, 13b => z < 175760
    w = inp[8]
    z, x = divmod(z, 26)
    if x - 9 != w:
        z = 26 * z + (w + 5)
        raise ValueError(f"8: {x-9} != {w}")

    # 10a, 11a, 12b, 13b => z < 10
    # 10a, 11b, 12a, 13b => z < 20
    # 10a, 11b, 12b, 13b => z < 260
    # 10b, 11a, 12a, 13b => z < 1
    # 10b, 11a, 12b, 13b => z < 260
    # 10b, 11b, 12a, 13b => z < 520
    # 10b, 11b, 12b, 13b => z < 6760
    z = 26 * z + (inp[9] + 7)

    # 10a: inp[10] != z % 26 - 15
    # 10b: inp[10] == z % 26 - 15
    # 10a, 11a, 12a, 13b => not possible
    # 10a, 11a, 12b, 13b => z < 260
    # 10a, 11b, 12a, 13b => z < 520
    # 10a, 11b, 12b, 13b => z < 6760
    # 10b, 11a, 12a, 13b => z < 26
    # 10b, 11a, 12b, 13b => z < 6760
    # 10b, 11b, 12a, 13b => z < 13520
    # 10b, 11b, 12b, 13b => z < 175760
    w = inp[10]
    z, x = divmod(z, 26)
    if x - 15 != w:
        z = 26 * z + (w + 6)
        raise ValueError(f"10: {x - 15} != {w}")

    # 11a: inp[11] != z % 26 - 7
    # 11a: inp[11] == z % 26 - 7
    # 11a, 12a, 13b => z == 0
    # 11a, 12b, 13b => z < 260
    # 11b, 12a, 13b => z < 520
    # 11b, 12b, 13b => z < 6760
    w = inp[11]
    z, x = divmod(z, 26)
    if x - 7 != w:
        z = 26 * z + (w + 8)
        raise ValueError(f"11: {x-7} != {w}")

    # 12a: inp[12] != z % 26 - 10
    # 12b: inp[12] == z % 26 - 10
    # 12a, 13b => z < 20
    # 12b, 13b => z < 260
    w = inp[12]
    z, x = divmod(z, 26)
    if x - 10 != w:
        z = 26 * z + (w + 4)
        raise ValueError(f"12: {x-10} != {w}")

    # 13a: inp[13] != z
    # 13b: inp[13] == z
    # 13a => not possible
    # 13b => z < 10
    w = inp[13]
    z, x = divmod(z, 26)
    if x + 0 != w:
        z = 26 * z + (w + 6)
        raise ValueError(f"13: {x+0} != {w}")

    # z == 0
    return z
