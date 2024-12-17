import dataclasses

from tools.tree import traverse_breath_first, for_sendable_generator

register: dict[str, int] = {
    'IP': 0,
}

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


# MY input
##########
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

# So every iteration, the 3 least significant bits of A are consumed
# They are mixed with some other parts of A[9:0], to produce the output
# Can we try to construct A 3 bits at a time, from least to most significant?


def lsf_to_int(lsb_first: list[int]) -> int:
    o = 0
    for i in reversed(lsb_first):
        o = o * 2 + i
    return o
def int_to_lsf(i: int) -> list[int]:
    l = []
    while i > 0:
        l.append(i%2)
        i = i // 2
    return l
def pad_list(l: list[int], length: int, padding: int = 0) -> list[int]:
    l = list(l)
    while len(l) < length:
        l.append(padding)
    return l


@dataclasses.dataclass
class State:
    A: list[int]
    output_so_far: int = 0

    def branches(self) -> list["State"]:
        next_output = program[self.output_so_far]
        opts = []
        for opt in self.options_for_output(next_output):
            try:
                combined_a = self.merge(self.A[(self.output_so_far * 3):], opt)
                opts.append(State(
                    [*self.A[:(self.output_so_far * 3)], *combined_a],
                    self.output_so_far + 1,
                ))
            except ValueError:
                pass
        return opts

    @staticmethod
    def options_for_output(b: int) -> list[list[int]]:
        assert 0 <= b < 8
        options = []
        for i in range(1024):
            _, out = my_program_iteration(i)
            if out == b:
                options.append(pad_list(int_to_lsf(i), 10))
        return options

    @staticmethod
    def merge(a: list[int], b: list[int]) -> list[int]:
        if len(a) < len(b):
            return State.merge(b, a)
        # we can now be sure len(a) >= len(b)
        out = []
        for i in range(len(b)):
            if a[i] != b[i]:
                raise ValueError()
            out.append(a[i])
        for i in range(len(b), len(a)):
            out.append(a[i])
        return out

    def output(self) -> list[int]:
        a = lsf_to_int(self.A)
        out = []
        while True:
            a, b = my_program_iteration(a)
            out.append(b)
            if a == 0:
                break
        return out


it = for_sendable_generator(traverse_breath_first(
    State([]),
    lambda s: s.branches(),
))
for node in it:
    output = node.output()
    if output == program:
        print(lsf_to_int(node.A))
        break
    print(node.A, output)
