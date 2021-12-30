"""
Incomplete!
"""

import enum
import math
import time
import typing

import psutil as psutil


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
        inp: typing.Optional[int] = None,
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
            inp,
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


class MultiTuple19:
    """
    Stores a bitmap of the matching values:
    1 => 1
    2 => 2
    3 => 4
    4 => 8
    5 => 16
    6 => 32
    7 => 64
    8 => 128
    9 => 256
    """
    def __init__(self, values: typing.Iterable[tuple] = None):
        if values is None:
            values = []
        self._values = list(values)

    @staticmethod
    def val_to_bitmap(v: int) -> int:
        return 2**(v-1)

    @staticmethod
    def set_to_bitmap(s: typing.Set[int]) -> int:
        bm = 0
        for v in s:
            bm |= MultiTuple19.val_to_bitmap(v)
        return bm

    @staticmethod
    def bitmap_to_set(bm: int) -> typing.Set[int]:
        s = set()
        for i in range(1, 9+1):
            if bm & 2**(i-1) != 0:
                s.add(i)
        return s

    def appended(self, suffix: tuple) -> "MultiTuple19":
        """
        Return a new MultiTuple19 with `suffix` appended to each stored value
        """
        bm_suffix = tuple([
            MultiTuple19.val_to_bitmap(_)
            for _ in suffix
        ])
        out = MultiTuple19()
        out._values = [
            v + bm_suffix
            for v in self._values
        ]
        return out

    def add(self, value: typing.Tuple[int, ...]):
        bm_value = [
            MultiTuple19.val_to_bitmap(_)
            for _ in value
        ]
        return self._add(bm_value)

    def _add(self, bm_value: typing.Tuple[int, ...]):
        """
        Add a single value to the set
        """
        def match_all_but_one(a: typing.Sized, b: typing.Sized) -> int:
            # if len(a) != len(b):
            #     return None

            mismatch = None
            for i in range(len(a)):
                if a[i] != b[i]:
                    if mismatch is None:
                        mismatch = i
                    else:  # already a mismatch, this is the second mismatch
                        return None
            return mismatch

        def replace_tuple_el(t: tuple, el_num: int, v: int) -> tuple:
            l = list(t)
            l[el_num] = v
            return tuple(l)

        for i, current_bm_value in enumerate(self._values):
            m = match_all_but_one(current_bm_value, bm_value)
            if m is not None:
                self._values[i] = replace_tuple_el(self._values[i], m, self._values[i][m] | bm_value[m])
                break
        else:
            self._values.append(bm_value)

    def extend(self, values: "MultiTuple19"):
        """
        Add multiple values to the set
        """
        if len(self._values) == 0:
            # Add them without checking. Checking was done before
            self._values.extend(values._values)
            return

        for bm_value in values._values:
            self._add(bm_value)


assert MultiTuple19.val_to_bitmap(5) == 16
assert MultiTuple19.set_to_bitmap({1, 2, 5}) == 19
assert MultiTuple19.bitmap_to_set(511) == {1, 2, 3, 4, 5, 6, 7, 8, 9}
mt = MultiTuple19()
mt.add((1, 2))
mt.add((1, 3))
mt = mt.appended((4,))
assert mt._values == [(1, 6, 8)]


class Multiverse:
    def __init__(self, register_state: typing.Tuple[int, int, int, int]):
        self.reality_inputs_map = {
            register_state: MultiTuple19([tuple()]),
        }
        self.num_inputs = 0

    def execute_instruction(self, instr_op: typing.Tuple[Instruction, typing.Iterable[typing.Union[Register, int]]]):
        instruction, operands = instr_op
        if instruction == Instruction.inp:
            self.num_inputs += 1

            # split up realities into 9 different ones
            new_reality_inputs_map = {}
            for reality, inputs in self.reality_inputs_map.items():
                for i in range(1, 9+1):
                    new_reality = execute_instruction(instr_op, reality, i)
                    new_reality_inputs_map.setdefault(new_reality, MultiTuple19()).extend(inputs.appended((i,)))
            self.reality_inputs_map = new_reality_inputs_map
            return

        if instruction == Instruction.add and operands[1] == 0:  # add _ 0  is noop
            return
        if instruction == Instruction.mul and operands[1] == 1:  # mul _ 1  is noop
            return
        if instruction == Instruction.div and operands[1] == 1:  # div _ 1  is noop
            return

        new_reality_inputs_map = {}
        for reality, inputs in self.reality_inputs_map.items():
            new_reality = execute_instruction(instr_op, reality)
            new_reality_inputs_map.setdefault(new_reality, MultiTuple19()).extend(inputs)
        self.reality_inputs_map = new_reality_inputs_map


with open("24.input.txt", "r") as f:
    program = read_in_program(f.read())
#program = program[0:100]  # Reduce runtime for profiling


m = Multiverse((0, 0, 0, 0))
program.append((Instruction.mul, (Register.w, 0)))
program.append((Instruction.mul, (Register.x, 0)))
program.append((Instruction.mul, (Register.y, 0)))
program.append((Instruction.eql, (Register.z, 0)))
for i, instr_op in enumerate(program):
    print(f"{i+1}  :  {instr_op}   ", end="", flush=True)
    tstart = time.time()
    m.execute_instruction(instr_op)
    dt = time.time() - tstart
    ram = psutil.Process().memory_info().rss / (1024 * 1024 * 1024)
    print(f"  => {len(m.reality_inputs_map)} realities, "
          f"{m.num_inputs} inputs, {ram:.1f} GB ram, {dt:.1f}s")

print(f"collapse  => {len(m.reality_inputs_map)} realities, "
      f"{m.num_inputs} inputs")

assert len(m.reality_inputs_map) <= 2
for regs, inputs in m.reality_inputs_map.items():
    if regs[3] == 1:
        break
else:
    raise RuntimeError("No reality with z==0")
print("Inputs that lead to z==0:")
for inp in inputs:
    print(inp)
