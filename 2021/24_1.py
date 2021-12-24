import abc
import enum
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


class Operand(abc.ABC):
    def __init__(self, input_info: typing.Set[typing.Tuple[int, int]] = None):
        if input_info is None:
            input_info = set()
        self.input_info = input_info

    @abc.abstractmethod
    def copy(self):
        raise NotImplementedError()

    def _combined_info(self, other) -> typing.Set[typing.Tuple[int, int]]:
        if not isinstance(other, Operand):
            raise ValueError(f"{repr(other)} is not an Operand")
        return self.input_info.union(other.input_info)

    def added_info(self, input_info: typing.Set[typing.Tuple[int, int]]) -> "Operand":
        o = self.copy()
        o.input_info = o.input_info.union(input_info)
        return o

    def __add__(self, other):
        if not isinstance(other, Operand):
            raise NotImplementedError()
        if isinstance(self, LiteralOperand) and isinstance(other, LiteralOperand):
            return LiteralOperand(self.value + other.value, self._combined_info(other))

        if isinstance(self, LiteralOperand) and self.value == 0:
            return other.added_info(self.input_info)
        if isinstance(other, LiteralOperand) and other.value == 0:
            return self.added_info(other.input_info)

        return Instruction.add, (self, other)

    def __mul__(self, other):
        if not isinstance(other, Operand):
            raise NotImplementedError()

        if isinstance(self, LiteralOperand) and isinstance(other, LiteralOperand):
            return LiteralOperand(self.value * other.value, self._combined_info(other))

        if isinstance(self, LiteralOperand) and self.value == 1:
            return other.added_info(self.input_info)
        if isinstance(other, LiteralOperand) and other.value == 1:
            return self.added_info(other.input_info)

        if isinstance(self, LiteralOperand) and self.value == 0:
            return self
        if isinstance(other, LiteralOperand) and other.value == 0:
            return other

        return Instruction.mul, (self, other)

    def __floordiv__(self, other):
        if not isinstance(other, Operand):
            raise NotImplementedError()

        if isinstance(self, LiteralOperand) and isinstance(other, LiteralOperand):
            # Python // rounds down; AoC requires round toward zero
            v = (abs(self.value) // other.value) * (-1 if self.value < 0 else 1)
            return LiteralOperand(v, self._combined_info(other))

        if isinstance(self, LiteralOperand) and self.value == 0:
            return self
        if isinstance(other, LiteralOperand) and other.value == 1:
            return self.added_info(other.input_info)

        return Instruction.div, (self, other)

    def __mod__(self, other):
        if not isinstance(other, Operand):
            raise NotImplementedError()

        if isinstance(self, LiteralOperand) and isinstance(other, LiteralOperand):
            return LiteralOperand(self.value % other.value, self._combined_info(other))

        if isinstance(self, LiteralOperand) and self.value == 0:
            return self

        if isinstance(other, LiteralOperand) and other.value == 1:
            return LiteralOperand(0, other.input_info)

        return Instruction.mod, (self, other)

    def eq(self, other):
        if not isinstance(other, Operand):
            raise NotImplementedError()

        if isinstance(self, LiteralOperand) and isinstance(other, LiteralOperand):
            value = 1 if self.value == other.value else 0
            return LiteralOperand(value, self._combined_info(other))

        if isinstance(self, Register) and isinstance(other, Register) and self.reg == other.reg:
            return LiteralOperand(1)

        return Instruction.eql, (self, other)


class LiteralOperand(Operand):
    def __init__(self, value, input_info: typing.Set[typing.Tuple[int, int]] = None):
        super().__init__(input_info=input_info)
        assert isinstance(value, int)
        self.value = value

    def copy(self) -> "LiteralOperand":
        return LiteralOperand(value=self.value, input_info=self.input_info)

    def __repr__(self) -> str:
        if len(self.input_info) == 0:
            return f"{self.value}"
        else:
            return f"<{self.value}>"


class RegisterOperand(Operand):
    def __init__(self, register: Register, input_info: typing.Set[typing.Tuple[int, int]] = None):
        super().__init__(input_info=input_info)
        self.reg = register

    def copy(self) -> "RegisterOperand":
        return RegisterOperand(register=self.reg)

    def __repr__(self) -> str:
        if len(self.input_info) == 0:
            return f"{self.reg.name}"
        else:
            return f"<{self.reg.name}>"


def read_in_program(code: str) -> typing.List[typing.Tuple[Instruction, typing.Tuple[Operand]]]:
    instructions = []
    for line in code.split('\n'):
        line = line.strip()
        if line == "":
            continue
        tokens = line.split()
        instruction = Instruction[tokens.pop(0)]
        num_operands = instruction.value[1]
        if len(tokens) != num_operands:
            raise ValueError(f"Expected {num_operands} operands for instruction {instruction.name}, got {len(tokens)}")
        for i, token in enumerate(tokens):
            try:
                token = RegisterOperand(Register[token])
            except KeyError:
                token = LiteralOperand(int(token))
            tokens[i] = token
        instructions.append((instruction, tuple(tokens)))
    return instructions


def replace_ast(ast, reg: Register, replacement):
    if isinstance(ast, RegisterOperand) and ast.reg == reg:
        if len(ast.input_info) > 0:
            return replacement.added_info(ast.input_info)
        else:
            return replacement
    elif isinstance(ast, Operand):
        return ast
    elif isinstance(ast, tuple) and len(ast) == 2:
        operands = tuple([
            replace_ast(op, reg, replacement)
            for op in ast[1]
        ])
        return ast[0], operands
    else:
        raise ValueError(f"Unknown ast node: {repr(ast)}")


def simplify_ast(ast):
    if isinstance(ast, Operand):
        return ast
    # else: instruction
    operand = tuple([
        simplify_ast(op)
        for op in ast[1]
    ])

    if ast[0] == 'or':
        nested_ops = set()
        for op in operand:
            if isinstance(op, tuple) and op[0] == 'or':  # flatten nested or
                for subop in op[1]:
                    nested_ops.add(subop)
            else:
                nested_ops.add(op)
        operand = list(nested_ops)

        non_false_op = []
        for op in operand:
            if isinstance(op, LiteralOperand) and op.value == 0:
                continue
            non_false_op.append(op)
        operand = tuple(non_false_op)
        if len(operand) == 0:
            return LiteralOperand(0)
        if len(operand) == 1:
            return operand[0]

    elif isinstance(operand[0], Operand) and isinstance(operand[1], Operand):
        if ast[0] == Instruction.add:
            return operand[0] + operand[1]

        elif ast[0] == Instruction.mul:
            return operand[0] * operand[1]

        elif ast[0] == Instruction.div:
            return operand[0] // operand[1]

        elif ast[0] == Instruction.mod:
            return operand[0] % operand[1]

        elif ast[0] == Instruction.eql:
            return operand[0].eq(operand[1])

    return ast[0], operand


input_num = 0
def step_backward(
        instruction_operands: typing.Tuple[Instruction, typing.Tuple[Operand]],
        ast,
):
    global input_num
    instruction, operand = instruction_operands
    if instruction == Instruction.inp:
        input_num -= 1
        ast = ('or', tuple([
            replace_ast(ast, operand[0].reg, LiteralOperand(i, {(input_num, i)}))
            for i in range(1, 9+1)  # 0 is not allowed
        ]))

    elif instruction == Instruction.add:
        ast = replace_ast(ast, operand[0].reg, operand[0] + operand[1])

    elif instruction == Instruction.mul:
        ast = replace_ast(ast, operand[0].reg, operand[0] * operand[1])

    elif instruction == Instruction.div:
        ast = replace_ast(ast, operand[0].reg, operand[0] // operand[1])

    elif instruction == Instruction.mod:
        ast = replace_ast(ast, operand[0].reg, operand[0] % operand[1])

    elif instruction == Instruction.eql:
        ast = replace_ast(ast, operand[0].reg, operand[0].eq(operand[1]))

    elif instruction == 'set':
        ast = replace_ast(ast, operand[0].reg, operand[1])

    else:
        raise NotImplementedError(f"{repr(instruction_operands)} not implemented")

    ast = simplify_ast(ast)
    return ast


with open("24.input.txt", "r") as f:
    program = read_in_program(f.read())
#print('\n'.join([str(_) for _ in program]))


ast = (Instruction.eql, (RegisterOperand(Register.z), LiteralOperand(0)))
print(f"     {ast}")
for i, instr_op in enumerate(reversed(program)):
    ast = step_backward(instr_op, ast)
    #print(f"{instr_op}  =>  {ast}")
    print(i)
for reg in Register:
    ast = step_backward(('set', (RegisterOperand(reg), LiteralOperand(0))), ast)
    #print(f"{reg.name}=0  =>  {ast}")

for i in ast[1]:
    print(i.input_info)
