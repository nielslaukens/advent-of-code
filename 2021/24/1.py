"""
Incomplete!
"""

import enum
import random
import typing

import puzzle_input

class Instruction(enum.Enum):
    inp = (enum.auto(), 1)
    add = (enum.auto(), 2)
    mul = (enum.auto(), 2)
    div = (enum.auto(), 2)
    mod = (enum.auto(), 2)
    eql = (enum.auto(), 2)

    def __repr__(self) -> str:
        return self.name


class Register(enum.Enum):
    w = 0
    x = 1
    y = 2
    z = 3

    def __repr__(self) -> str:
        return self.name


def read_in_program(code: str) -> typing.List[typing.Tuple[Instruction, typing.List]]:
    instructions = []
    for line in code.split('\n'):
        line = line.strip()
        if line == "":
            continue
        if '#' in line:
            line = line[0:(line.index('#'))]
        tokens = line.split()
        instruction = Instruction[tokens.pop(0)]
        num_operands = instruction.value[1]
        if len(tokens) != num_operands:
            raise ValueError(f"Expected {num_operands} operands for instruction {instruction.name}, got {len(tokens)}")
        for i, token in enumerate(tokens):
            try:
                token = Register[token]
            except KeyError:
                token = int(token)
            tokens[i] = token
        instructions.append((instruction, tokens))
    return instructions


def execute_instruction(
        instr_op: typing.Tuple[Instruction, typing.Iterable[typing.Union[Register, int]]],
        register_state: typing.Tuple[int, int, int, int],
        inp: typing.List[int],
) -> typing.Tuple[int, int, int, int]:
    instruction, operands = instr_op

    def reg_or_imm(op: typing.Union[Register, int]) -> int:
        if isinstance(op, Register):
            return register_state[op.value]
        else:
            return op

    def set_reg(
            register_state: typing.Tuple[int, int, int, int],
            reg: Register,
            value: int
    ) -> typing.Tuple[int, int, int, int]:
        register_state = list(register_state)
        register_state[reg.value] = value
        return tuple(register_state)

    if instruction == Instruction.inp:
        if inp is None:
            raise ValueError("INP instruction, but no input supplied ")
        register_state = set_reg(
            register_state, operands[0],
            inp.pop(0),
        )
    elif instruction == Instruction.add:
        register_state = set_reg(
            register_state, operands[0],
            register_state[operands[0].value] + reg_or_imm(operands[1])
        )
    elif instruction == Instruction.mul:
        register_state = set_reg(
            register_state, operands[0],
            register_state[operands[0].value] * reg_or_imm(operands[1])
        )
    elif instruction == Instruction.div:
        # Python // rounds towards -inf; AoC div rounds toward zero
        op1 = register_state[operands[0].value]
        op2 = reg_or_imm(operands[1])
        v = abs(op1) // abs(op2)
        v *= (-1 if op1 < 0 else 1) * (-1 if op2 < 0 else 1)
        register_state = set_reg(
            register_state, operands[0],
            v
        )
    elif instruction == Instruction.mod:
        register_state = set_reg(
            register_state, operands[0],
            register_state[operands[0].value] % reg_or_imm(operands[1])
        )
    elif instruction == Instruction.eql:
        v = 1 if register_state[operands[0].value] == reg_or_imm(operands[1]) else 0
        register_state = set_reg(
            register_state, operands[0],
            v
        )
    else:
        raise ValueError(f"Unknown instruction {instruction}")

    return register_state

# 3b, 7b, 8b, 10b, 11b, 12b, 13b
#      0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13
inp = [2, 9, 5, 9, 9, 4, 6, 9, 9, 9, 1, 7, 3, 9]
z = puzzle_input.run(inp)
print(z)


#      0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13
inp = [1, 7, 1, 5, 3, 1, 1, 4, 6, 9, 1, 1, 1, 8]
z = puzzle_input.run(inp)
print(z)
