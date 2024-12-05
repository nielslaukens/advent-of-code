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


def create_graph(pages_after_page: dict[int, set[int]], keep_pages: set[int] | None = None) -> tuple[dict[int, int], dict[int, int]]:
    # WARNING: the resulting graph can be CYCLIC!
    # simplify the graph by excluding pages further away
    next_page: dict[int, int] = {}
    prev_page: dict[int, int] = {}
    for before, afters in pages_after_page.items():
        if keep_pages is not None and before not in keep_pages:
            continue
        pages_more_than_1_away = set()
        if keep_pages is not None:
            afters = afters.intersection(keep_pages)
        for after in afters:
            after_afters = pages_after_page.get(after, set())
            pages_more_than_1_away.update(after_afters)
        directly_next_page = afters.difference(pages_more_than_1_away)
        if len(directly_next_page) == 1:
            directly_next_page = next(iter(directly_next_page))
            assert before not in next_page
            assert directly_next_page not in prev_page
            next_page[before] = directly_next_page
            prev_page[directly_next_page] = before
        elif len(directly_next_page) == 0:
            pass
        else:
            raise RuntimeError("Unexpected: multiple pages left")
    return next_page, prev_page


def walk_until_end(next_dict: dict[int, int], start_node: int) -> int:
    candidate = next(iter(next_dict.keys()))  # pick random page
    seen = [candidate]
    while True:  # walk backwards
        _ = next_dict.get(candidate)
        if _ is None:
            return candidate
        candidate = _
        if candidate in seen:
            raise RuntimeError(f"Cyclic: {seen} + {candidate}")
        seen.append(candidate)


sum_middle_pages = 0
for i, print_job in enumerate(pages_to_produce):
    next_page, prev_page = create_graph(page_ordering_rules, keep_pages=set(print_job))

    page = walk_until_end(prev_page, print_job[0])
    ordered_job = [page]
    while True:
        page = next_page.get(page)
        if page is not None:
            ordered_job.append(page)
        else:
            break

    if ordered_job != print_job:
        assert len(ordered_job) % 2 == 1  # assume odd number of pages
        middle_page = ordered_job[len(ordered_job)//2]
        sum_middle_pages += middle_page

print(sum_middle_pages)
