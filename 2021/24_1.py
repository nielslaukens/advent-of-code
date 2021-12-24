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


def read_in_program(code: str) -> typing.List[typing.Tuple[Instruction, typing.List[Operand]]]:
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
                token = Register[token]
            except KeyError:
                token = int(token)
            tokens[i] = token
        instructions.append((instruction, tokens))
    return instructions


def execute_program(
        instructions: typing.List[typing.Tuple[Instruction, typing.List]],
        input_data: typing.List[int],
):
    registers = {
        k: 0
        for k in Register
    }

    def reg_or_imm(op):
        if isinstance(op, Register):
            return registers[op]
        else:
            return op

    for instruction, operands in instructions:
        if instruction == Instruction.inp:
            registers[operands[0]] = input_data.pop(0)
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
            if op0 < 0 or op1 <= 0:
                raise ValueError(f"Modulo of/with negative number")
            registers[operands[0]] = op0 % op1
        elif instruction == Instruction.eql:
            registers[operands[0]] = 1 if registers[operands[0]] == reg_or_imm(operands[1]) else 0
    return registers


class FromInput(int):
    def __new__(cls, value, input_info: typing.List[str]) -> "FromInput":
        o = super().__new__(cls, value)
        assert len(input_info) > 0
        o.input_info = input_info
        return o

    def __repr__(self) -> str:
        return "<" + str(int(self)) + ">"

    def _combined_info(self, other):
        info = self.input_info
        if isinstance(other, FromInput):
            info += other.input_info
        return info

    def __add__(self, other):
        return FromInput(int(self) + int(other), self._combined_info(other))

    def __radd__(self, other):
        return self.__add__(other)  # commutative

    def __mul__(self, other):
        return FromInput(int(self) * int(other), self._combined_info(other))

    def __rmul__(self, other):
        return self.__mul__(other)  # commutative

    def __floordiv__(self, other):
        return FromInput(int(self) // int(other), self._combined_info(other))

    def __rfloordiv__(self, other):
        return FromInput(int(other) // int(self), self._combined_info(other))

    def __mod__(self, other):
         return FromInput(int(self) % int(other), self._combined_info(other))

    def __rmod__(self, other):
        return FromInput(int(other) % int(self), self._combined_info(other))

    @staticmethod
    def eq(a, b) -> int:
        input_info = []
        if isinstance(a, FromInput):
            input_info += a.input_info
        if isinstance(b, FromInput):
            input_info += b.input_info

        value = 1 if int(a) == int(b) else 0
        if len(input_info) > 0:
            return FromInput(value, input_info)
        else:
            return value

    @classmethod
    def maybe(cls, value, input_info):
        if isinstance(input_info, FromInput):
            return FromInput(value, input_info.input_info)
        else:
            return value


def replace_ast(
        ast,
        reg: Register,
        replacement,
):
    if ast == reg:
        return replacement
    if isinstance(ast, int) or isinstance(ast, Register):
        return ast
    if isinstance(ast, tuple):
        operands = [
            replace_ast(op, reg, replacement)
            for op in ast[1]
        ]
        return ast[0], operands
    raise ValueError(f"Unknown ast node: {ast}")


def simplify_ast(ast):
    if isinstance(ast, int) or isinstance(ast, Register):
        return ast
    elif isinstance(ast, tuple):
        op = [
            simplify_ast(op)
            for op in ast[1]
        ]

        if len(op) == 2 and isinstance(op[0], int) and isinstance(op[1], int):
            if ast[0] == Instruction.add:
                return op[0] + op[1]
            elif ast[0] == Instruction.mul:
                return op[0] * op[1]
            elif ast[0] == Instruction.div:
                return op[0] // op[1]
            elif ast[0] == Instruction.mod:
                return op[0] % op[1]
            elif ast[0] == Instruction.eql:
                return FromInput.eq(op[0], op[1])

        if ast[0] == Instruction.add:
            if op[0] == 0:
                return FromInput.maybe(value=op[1], input_info=op[0])
            if op[1] == 0:
                return FromInput.maybe(value=op[0], input_info=op[1])

        if ast[0] == Instruction.mul:
            if op[0] == 0:
                return FromInput.maybe(0, op[0])
            if op[1] == 0:
                return FromInput.maybe(0, op[1])
            if op[0] == 1:
                return FromInput.maybe(op[1], op[0])
            if op[1] == 1:
                return FromInput.maybe(op[0], op[1])

        if ast[0] == 'eq' or ast[0] == 'ne':
            if op[0] == op[1]:
                return 1 if ast[0] == 'eq' else 0
            if isinstance(op[0], int) and isinstance(op[1], int) and op[0] != op[1]:
                return 0 if ast[0] == 'eq' else 1

        if ast[0] == 'and':
            non_true_op = []
            for operand in op:
                if operand == 0:  # any single operand False means 0
                    return 0
                if operand != 1:
                    non_true_op.append(operand)
            op = non_true_op
            if len(op) == 0:
                return 1
            if len(op) == 1:
                return op[0]
        if ast[0] == 'or':
            non_false_op = []
            for operand in op:
                if isinstance(operand, int) and operand != 0:  # any single operand True means 1
                    return 1
                if operand != 0:
                    non_false_op.append(operand)
            op = non_false_op
            if len(op) == 0:
                return 0
            if len(op) == 1:
                return op[0]

        return ast[0], op
    raise ValueError(f"Unknown ast node: {ast}")


input_num = 14
def step_backward(
        instruction_operands: typing.Tuple[Instruction, typing.List],
        constraints_ast,
):
    global input_num
    instruction, operands = instruction_operands
    if instruction == Instruction.inp:
        constraints_ast = ('or', [
            replace_ast(constraints_ast, operands[0], FromInput(i, [f"Input {input_num} = {i}"]))
            for i in range(1, 9+1)
        ])
        input_num -= 1
    elif instruction == Instruction.add:
        if operands[1] == 0:  # noop
            pass
        else:
            constraints_ast = replace_ast(constraints_ast, operands[0], (Instruction.add, [operands[0], operands[1]]))
    elif instruction == Instruction.mul:
        if operands[1] == 0:  # kill
            constraints_ast = replace_ast(constraints_ast, operands[0], 0)
        elif operands[1] == 1:  # noop
            pass
        else:
            constraints_ast = replace_ast(constraints_ast, operands[0], (Instruction.mul, [operands[0], operands[1]]))
    elif instruction == Instruction.eql:
        constraints_ast = ('or', [
            ('and', [('eq', [operands[0], operands[1]]), replace_ast(constraints_ast, operands[0], 0)]),
            ('and', [('ne', [operands[0], operands[1]]), replace_ast(constraints_ast, operands[0], 1)]),
        ])
    elif instruction == Instruction.div:
        if operands[1] == 1:  # noop
            pass
        else:
            constraints_ast = replace_ast(constraints_ast, operands[0], (Instruction.div, [operands[0], operands[1]]))
    elif instruction == Instruction.mod:
        if operands[1] == 1:  # %1 => 0
            constraints_ast = replace_ast(constraints_ast, operands[0], 0)
        else:
            constraints_ast = replace_ast(constraints_ast, operands[0], (Instruction.mod, [operands[0], operands[1]]))
    elif instruction == 'set':
        constraints_ast = replace_ast(constraints_ast, operands[0], operands[1])
    else:
        raise ValueError(f"unknown instruction: {instruction_operands}")
    constraints_ast = simplify_ast(constraints_ast)
    return constraints_ast


with open("24.input.txt", "r") as f:
    program = read_in_program(f.read())


program = read_in_program("""\
inp w
add w -1
add z w
""")
constraints = (Instruction.eql, [Register.z, 0])
for instr in reversed(program):
    constraints = step_backward(instr, constraints)
    print(f"{instr}  =>  {constraints}")
for reg in Register:
    constraints = step_backward(('set', [reg, 0]), constraints)
    print(f"=>  {constraints}")

#print('\n'.join([str(_) for _ in program]))
model_number = 0
model_number_str = f"{model_number:014d}"
input_data = [int(_) for _ in model_number_str]
if '0' in input_data:
    result = False
else:
    result = execute_program(program, input_data)
    result = result[Register.z] == 0
print(f"Model number {model_number} is {'valid' if result else 'invalid'}")
