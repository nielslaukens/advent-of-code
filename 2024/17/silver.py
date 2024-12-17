import re

register: dict[str, int] = {
    'IP': 0,
}
with open('input.txt') as f:
    state = 'registers'
    for line in f:
        line = line.strip()
        if line == "":
            state = 'program'
            continue
        if state == 'registers':
            m = re.match(r'^Register ([ABC]): (\d+)$', line)
            assert m
            register[m.group(1)] = int(m.group(2))
        elif state == 'program':
            assert line.startswith("Program: ")
            program = line[len("Program: "):]
            program = [
                int(_)
                for _ in program.split(',')
            ]

print(register)
print(program)

instructions = {}


def combo(operand: int) -> int:
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return register['A']
    if operand == 5:
        return register['B']
    if operand == 6:
        return register['C']
    if operand == 7:
        raise RuntimeError('invalid combo operand 7')

def adv(operand: int) -> None:
    """
    The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The
    denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would
    divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated
    to an integer and then written to the A register.
    """
    operand = combo(operand)
    register['A'] = register['A'] // (2**operand)
instructions[0] = adv

def bxl(operand: int) -> None:
    """
    The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then
    stores the result in register B.
    """
    register['B'] = register['B'] ^ operand
instructions[1] = bxl

def bst(operand: int) -> None:
    """
    The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3
    bits), then writes that value to the B register.
    """
    operand = combo(operand)
    register['B'] = operand % 8
instructions[2] = bst

def jnz(operand: int) -> None:
    """
    The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps
    by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction
    pointer is not increased by 2 after this instruction.
    """
    if register['A'] == 0:
        return
    register['IP'] = operand - 2  # compensate for next instruction
instructions[3] = jnz

def bxc(operand: int) -> None:
    """
    The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in
    register B. (For legacy reasons, this instruction reads an operand but ignores it.)
    """
    register['B'] = register['B'] ^ register['C']
instructions[4] = bxc

def out(operand: int) -> int:
    """
    The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a
    program outputs multiple values, they are separated by commas.)
    """
    operand = combo(operand)
    return operand % 8
instructions[5] = out

def bdv(operand: int) -> None:
    """
    The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B
    register. (The numerator is still read from the A register.)
    """
    operand = combo(operand)
    register['B'] = register['A'] // (2**operand)
instructions[6] = bdv

def cdv(operand: int) -> None:
    """
    The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C
    register. (The numerator is still read from the A register.)
    """
    operand = combo(operand)
    register['C'] = register['A'] // (2**operand)
instructions[7] = cdv

def step():
    ip = register['IP']
    instruction, operand = program[ip:ip+2]
    out = instructions[instruction](operand)
    register['IP'] = register['IP'] + 2
    return out

def run():
    out = []
    while register['IP'] < len(program):
        step_out = step()
        if step_out is not None:
            out.append(step_out)
    return out

if False:
    # If register C contains 9, the program 2,6 would set register B to 1.
    register = {'IP': 0, 'C': 9}
    program = [2, 6]
    run()
    assert register['B'] == 1

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    register = {'IP': 0, 'A': 10}
    program = [5, 0, 5, 1, 5, 4]
    out = run()
    assert out == [0, 1, 2]

    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    register = {'IP': 0, 'A': 2024}
    program = [0, 1, 5, 4, 3, 0]
    out = run()
    assert register['A'] == 0
    assert out == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]

    # If register B contains 29, the program 1,7 would set register B to 26.
    register = {'IP': 0, 'B': 29}
    program = [1, 7]
    out = run()
    assert register['B'] == 26

    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    register = {'IP': 0, 'B': 2024, 'C': 43690}
    program = [4, 0]
    out = run()
    assert register['B'] == 44354


out = run()
print(','.join(str(_) for _ in out))
