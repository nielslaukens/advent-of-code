page_ordering_rules_before: dict[int, int] = {}
page_ordering_rules_after: dict[int, int] = {}
pages_to_produce: list[list[int]] = []

with open("input.txt", "r") as f:
    state = 'page_ordering'
    while line := f.readline():
        line = line.strip()
        if line == "":
            state = 'produce'
            continue
        if state == 'page_ordering':
            before, after = line.split('|')
            before = int(before)
            after = int(after)
            page_ordering_rules_before[after] = before
            page_ordering_rules_after[before] = after
        elif state == 'produce':
            pages = [int(page) for page in line.split(',')]
            pages_to_produce.append(pages)

print("before: ", page_ordering_rules_before)
print("after: ", page_ordering_rules_after)
print(pages_to_produce)

# ASSUMPTION: every page in pages_to_reproduce has a rule
for print_job in pages_to_produce:
    for page in print_job:
        if page not in page_ordering_rules_after and page not in page_ordering_rules_before:
            raise RuntimeError(f"Assumption not valid: {page} has no rule")

sum_middle_pages = 0
for i, print_job in enumerate(pages_to_produce):
    print(f"checking print job {i+1}: {print_job}")
    all_ok = True
    for before, after in page_ordering_rules_after.items():
        try:
            before_pos = print_job.index(before)
            after_pos = print_job.index(after)
            if before_pos > after_pos:
                all_ok = False
                break
        except ValueError:  # before and/or after not in print_job
            # rule does not apply
            pass

    if all_ok:
        assert len(print_job) % 2 == 1  # assume odd number of pages
        middle_page = print_job[len(print_job)//2]
        sum_middle_pages += middle_page

print(f"Sum middle pages: {sum_middle_pages}")
# 6050 too high
