"""
Incomplete!
"""

import enum
import math
import typing


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
    w = enum.auto()
    x = enum.auto()
    y = enum.auto()
    z = enum.auto()

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


class DidNothing(Exception):
    pass


class Ast:
    def __init__(self, operation, operands):
        self.operation = operation
        self.operands = operands

    def min(self):
        if self.operation == '=':
            return self.operands

        if self.operation == '$':
            return 1

        if self.operation == '+':
            res = None
            for op in self.operands:
                m = op.min()
                if m is None:
                    return None

                if res is None:
                    res = m
                else:
                    res += m
            return res

        if self.operation == '?':
            return 0

        return None

    def max(self):
        if self.operation == '=':
            return self.operands

        if self.operation == '$':
            return 9

        if self.operation == '+':
            res = None
            for op in self.operands:
                m = op.max()
                if m is None:
                    return None
                if res is None:
                    res = m
                else:
                    res += m
            return res

        if self.operation == '?':
            return 1

        return None

    def __repr__(self) -> str:
        if self.operation == '=' or self.operation == '$':
            return str(self.operands)
        ops = [
            repr(op)
            for op in self.operands
        ]
        return self.operation + '(' + ', '.join([repr(_) for _ in self.operands]) + ')'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Ast):
            return False
        if self.operation != other.operation:
            return False
        return self.operands == other.operands

    def _is_eq(self, num):
        return self.operation == '=' and self.operands == num

    def __add__(self, other) -> "Ast":
        if self._is_eq(0):
            return other
        if other._is_eq(0):
            return self

        if self.operation == '=' and other.operation == '=':
            return Ast('=', self.operands + other.operands)

        operands = []
        if self.operation == '+':
            operands.extend(self.operands)
        else:
            operands.append(self)
        if other.operation == '+':
            operands.extend(other.operands)
        else:
            operands.append(other)
        literals = 0
        non_literals = []
        for op in operands:
            if op.operation == '=':
                literals += op.operands
            else:
                non_literals.append(op)
        if literals != 0:
            non_literals.insert(0, Ast('=', literals))
        return Ast('+', tuple(non_literals))

    def __mul__(self, other) -> "Ast":
        if self._is_eq(0):
            return self
        if other._is_eq(0):
            return other

        if self._is_eq(1):
            return other
        if other._is_eq(1):
            return self

        if self.operation == '=' and other.operation == '=':
            return Ast('=', self.operands * other.operands)

        operands = []
        if self.operation == '*':
            operands.extend(self.operands)
        else:
            operands.append(self)
        if other.operation == '*':
            operands.extend(other.operands)
        else:
            operands.append(other)
        literals = 1
        non_literals = []
        for op in operands:
            if op.operation == '=':
                literals *= op.operands
            else:
                non_literals.append(op)
        if literals != 1:
            non_literals.insert(0, Ast('=', literals))
        return Ast('*', tuple(non_literals))

    def __floordiv__(self, other):
        if self._is_eq(0):
            return self

        if other._is_eq(1):
            return self

        if self.operation == '=' and other.operation == '=':
            if other.operands == 0:
                raise ValueError("Divide by 0")

            # Instructions say div is rounded toward 0, Python's // rounds toward -inf
            v = (abs(self.operands) // other.operands) * (-1 if self.operands < 0 else 1)
            return Ast('=', v)

        if self.operation == '*' \
                and self.operands[0].operation == '=' and other.operation == '=' \
                and self.operands[0].operands == other.operands:
            # (N * x) / N  => x
            return self.operands[1]

        return Ast('/', (self, other))

    def __mod__(self, other):
        if self._is_eq(0):
            return self

        if other._is_eq(1):
            return Ast('=', 0)

        if self.operation == '=' and other.operation == '=':
            if other.operands <= 0:
                raise ValueError(f"Mod % {other.operands} not valid")
            return Ast('=', self.operands % other.operands)

        if self.operation == '$' and other.operation == '=':
            if other.operands >= 10:
                # var is 1-9. Modulo 10 or above is a noop
                return self

        return Ast('%', (self, other))

    def eq(self, other):
        if self.operation == '=' and other.operation == '=':
            if self.operands == other.operands:
                return Ast('=', 1)
            else:
                return Ast('=', 0)

        s_min = self.min()
        s_max = self.max()
        o_min = other.min()
        o_max = other.max()
        if s_min is not None and s_max is not None and o_min is not None and o_max is not None:
            if s_min == s_max == o_min == o_max:
                return Ast('=', 1)
            if s_max < o_min:
                return Ast('=', 0)
            if o_max < s_min:
                return Ast('=', 0)

        return Ast('?', (self, other))

    def simplify(self) -> "Ast":
        if self.operation == '%' and self.operands[0].operation == '+' and self.operands[1].operation == '=':
            # (a + b) % c  =>  a%c + b%c
            total = Ast('=', 0)
            for op in self.operands[0].operands:
                term = (op % self.operands[1]).simplify()
                total = total + term
            return total

        if self.operation == '%' and self.operands[0].operation == '*' and self.operands[1].operation == '=':
            # (a * b) % c  =>  if a % c == 0 then 0
            # (we already pulled literals to the front, so we don't need to check b
            if self.operands[0].operands[0].operation == '=' and \
                    self.operands[0].operands[0].operands % self.operands[1].operands == 0:
                return Ast('=', 0)

        if self.operation == '*' and self.operands[1].operation == '+' and \
                self.operands[0].operation == '=':
            # (a * (b + c))  =>  ((a*b) + (a*c))
            total = Ast('=', 0)
            for op in self.operands[1].operands:
                term = (self.operands[0] * op).simplify()
                total = total + term
            return total

        return self


assert Ast('=', 0) == Ast('=', 0)

assert Ast('=', 0) + Ast('=', 0) == Ast('=', 0)
assert Ast('=', 0) + Ast('=', 1) == Ast('=', 1)
assert Ast('=', 1) + Ast('=', 2) == Ast('=', 3)
assert Ast('$', 'a') + Ast('=', 0) == Ast('$', 'a')
assert Ast('=', 0) + Ast('$', 'a') == Ast('$', 'a')
assert Ast('$', 'a') + Ast('$', 'b') + Ast('$', 'c') == Ast('+', (Ast('$', 'a'), Ast('$', 'b'), Ast('$', 'c')))
assert Ast('=', 2) + Ast('$', 'a') + Ast('=', 3) == Ast('+', (Ast('=', 5), Ast('$', 'a')))

assert Ast('=', 0) * Ast('$', 'a') == Ast('=', 0)
assert Ast('=', 1) * Ast('$', 'a') == Ast('$', 'a')
assert Ast('=', 2) * Ast('$', 'a') * Ast('=', 2) == Ast('*', (Ast('=', 4), Ast('$', 'a')))

# note: 26 * (a / 26)  is not equal to `a`, since it's floordiv!
assert Ast('*', (Ast('=', 26), Ast('$', 'a'))) // Ast('=', 26) == Ast('$', 'a')


def execute_program(
        instructions: typing.List[typing.Tuple[Instruction, typing.List]],
        input_data: typing.List[int],
):
    registers = {
        k: Ast('=', 0)
        for k in Register
    }

    def reg_or_imm(op):
        if isinstance(op, Register):
            return registers[op]
        else:
            return Ast('=', op)

    for i, i_o in enumerate(instructions):
        instruction, operands = i_o
        if instruction == Instruction.inp:
            registers[operands[0]] = Ast('$', input_data.pop(0))
        elif instruction == Instruction.add:
            registers[operands[0]] = registers[operands[0]] + reg_or_imm(operands[1])
        elif instruction == Instruction.mul:
            registers[operands[0]] = registers[operands[0]] * reg_or_imm(operands[1])
        elif instruction == Instruction.div:
            op1 = reg_or_imm(operands[1])
            if op1 == 0:
                raise ValueError(f"Divide by zero")
            registers[operands[0]] = registers[operands[0]] // op1
        elif instruction == Instruction.mod:
            op0 = registers[operands[0]]
            op1 = reg_or_imm(operands[1])
            registers[operands[0]] = op0 % op1
        elif instruction == Instruction.eql:
            registers[operands[0]] = registers[operands[0]].eq(reg_or_imm(operands[1]))

        for reg_n in registers.keys():
            registers[reg_n] = registers[reg_n].simplify()

        #print()
        #print(f"{i+1} {instruction.name} {operands}")
        #for reg_n, reg_v in registers.items():
        #    print(f"{reg_n} = {reg_v}")
    return registers


with open("24.input.txt", "r") as f:
    program = read_in_program(f.read())

regs = execute_program(program, [chr(ord('a') + _) for _ in range(14)])
z = regs[Register.z]
print('forward done')
