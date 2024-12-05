page_ordering_rules: dict[int, set[int]] = {}
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
            page_ordering_rules.setdefault(before, set())
            page_ordering_rules[before].add(after)
        elif state == 'produce':
            pages = [int(page) for page in line.split(',')]
            pages_to_produce.append(pages)

print("after rules: ", page_ordering_rules)
print(pages_to_produce)

sum_middle_pages = 0
for i, print_job in enumerate(pages_to_produce):
    print(f"checking print job {i+1}: {print_job}")
    all_ok = True
    for before, afters in page_ordering_rules.items():
        for after in afters:
            try:
                before_pos = print_job.index(before)
                after_pos = print_job.index(after)
                if before_pos > after_pos:
                    print(f"  {before} at {before_pos} is not before {after} at {after_pos}")
                    all_ok = False
                    break
            except ValueError:  # before and/or after not in print_job
                # rule does not apply
                pass
        if not all_ok:
            break

    if all_ok:
        assert len(print_job) % 2 == 1  # assume odd number of pages
        middle_page = print_job[len(print_job)//2]
        sum_middle_pages += middle_page

print(f"Sum middle pages: {sum_middle_pages}")
