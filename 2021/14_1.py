import re

with open("14.sample.txt", "r") as f:
    chain = f.readline().strip()
    _ = f.readline().strip()
    assert _ == ""
    pair_insertion_rules = {}
    for line in f.readlines():
        line = line.strip()
        pir = line.split(' -> ')
        pair_insertion_rules[pir[0]] = pir[1]


def step(chain: str) -> str:
    pattern = '|'.join([p[0] + '(?=' + p[1] + ')' for p in pair_insertion_rules.keys()])
    def insert(match) -> str:
        match_pos = match.regs[0][0]
        matched_pair = match.string[match_pos:(match_pos+2)]
        return matched_pair[0] + pair_insertion_rules[matched_pair]
    chain = re.sub(
        pattern,
        insert,
        chain,
    )
    return chain


print(chain)
for steps in range(10):
    chain = step(chain)
    print(chain)
print(f"chain length: {len(chain)}")
element_count = {}
for e in chain:
    element_count[e] = element_count.get(e, 0) + 1
print(element_count)

print(f"score: {max(element_count.values()) - min(element_count.values())}")