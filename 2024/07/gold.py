import enum
import itertools

equations: list[tuple[int, list[int]]] = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        result, components = line.split(":")
        result = int(result)
        components = [int(_) for _ in components.split()]
        equations.append((result, components))


class Operator(enum.Enum):
    ADD = '+'
    MULTIPLY = '*'
    CONCATENATE = '||'


sum_results_of_true_equations = 0
for result, components in equations:
    operator_positions = len(components) - 1
    print(result, components)
    for operators in itertools.product(Operator, repeat=operator_positions):
        calculated_result = components[0]
        for i, operator in enumerate(operators):
            if operator == Operator.ADD:
                calculated_result += components[i+1]
            elif operator == Operator.MULTIPLY:
                calculated_result *= components[i+1]
            elif operator == Operator.CONCATENATE:
                calculated_result = int(str(calculated_result) + str(components[i+1]))
            else:
                raise RuntimeError("Unreachable")
        if result == calculated_result:
            print(" !! ", operators, calculated_result)
            sum_results_of_true_equations += result
            break  # no need to check further

print(f"Sum of results: {sum_results_of_true_equations}")
