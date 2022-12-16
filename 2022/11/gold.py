import dataclasses
import re

import typing


@dataclasses.dataclass
class Monkey:
    items: list[int] = dataclasses.field(default_factory=list)
    operation: typing.Callable[[int], int] = lambda x: x
    test_mod: int = None
    next_monkey: dict[bool, int] = dataclasses.field(default_factory=dict)


monkeys: dict[int, Monkey] = {}
monkey = None
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('Monkey'):
            monkey = int(line[(len('Monkey ')):-1])
            monkeys[monkey] = Monkey()

        elif line.startswith('  Starting items:'):
            items = [
                int(_)
                for _ in line[len('  Starting items: '):].split(',')
            ]
            monkeys[monkey].items = items.copy()

        elif line.startswith('  Operation: new = '):
            op = line[len('  Operation: new = '):]
            def close_over_op(op):
                return lambda old: eval(op.replace('old', str(old)))
            monkeys[monkey].operation = close_over_op(op)

        elif line.startswith('  Test: '):
            t = line[len('  Test: '):]
            if t.startswith('divisible by '):
                d = int(t[len('divisible by '):])
            else:
                raise ValueError(f"Unknown Test: {t}")
            monkeys[monkey].test_mod = d

        elif line.startswith('    If'):
            match = re.match(r'    If (true|false): throw to monkey (\d+)', line)
            if not match:
                raise ValueError(f"Did not understand: {line}")
            condition = match.group(1) == 'true'
            monkeys[monkey].next_monkey[condition] = int(match.group(2))

        elif line == "":
            pass

        else:
            raise ValueError(f"? `{line}`")


all_monkey_mod = 1
for monkey in monkeys.values():
    all_monkey_mod *= monkey.test_mod
print(f"All monkey mod: {all_monkey_mod}")


num_of_inspections: dict[int, int] = {
    _: 0
    for _ in monkeys.keys()
}
for round_ in range(10_000):
    for monkey_nr in sorted(monkeys.keys()):
        monkey = monkeys[monkey_nr]
        for item in monkey.items:
            #print(f"Monkey {monkey_nr} inspecting item with worry level {item.worry_level}")
            num_of_inspections[monkey_nr] += 1
            nwl = monkey.operation(item)
            #print(f"  New worry level: {nwl}")
            item = nwl % all_monkey_mod
            test_outcome = item % monkey.test_mod == 0
            next_monkey = monkey.next_monkey[test_outcome]
            #print(f"  Test: {test_outcome} => throw to {next_monkey}")
            monkeys[next_monkey].items.append(item)
        monkey.items = []

    #print()
    #print(f"after round {round_+1}")
    #for monkey_nr in sorted(monkeys.keys()):
    #    print(f"Monkey {monkey_nr}: {monkeys[monkey_nr].items}")

    #print(f"{round_+1}: {num_of_inspections}")

print(num_of_inspections)
sorted_num_inspections = sorted(num_of_inspections.values(), reverse=True)
monkey_business = sorted_num_inspections[0] * sorted_num_inspections[1]
print(f"Monkey Business: {monkey_business}")
