import itertools

with open("input.txt", "r") as f:
    reports = f.readlines()

for i, report in enumerate(reports):
    levels = [
        int(level)
        for level in report.split()
    ]
    reports[i] = levels


def is_report_safe(report: list[int]) -> bool:
    direction = None
    for level1, level2 in itertools.pairwise(report):
        if level1 == level2:
            return False
        elif level1 < level2:
            pair_direction = "up"
        else:
            pair_direction = "down"

        if direction is None:
            direction = pair_direction
        if direction != pair_direction:
            return False

        diff = abs(level1 - level2)
        if not 1 <= diff <= 3:
            return False
    return True


def problem_damper(report: list[int]) -> bool:
    if is_report_safe(report):
        return True
    for i in range(len(report)):
        modified_report = [*report[0:i], *report[(i+1):]]
        #print(report, i, modified_report)
        if is_report_safe(modified_report):
            return True
    return False


safe_reports = 0
for report in reports:
    safe = problem_damper(report)
    print(report, safe)
    if safe:
        safe_reports += 1
print(safe_reports)
