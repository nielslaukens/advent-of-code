import re

with open("14.input.txt", "r") as f:
    chain = f.readline().strip()
    _ = f.readline().strip()
    assert _ == ""
    pair_insertion_rules = {}
    for line in f.readlines():
        line = line.strip()
        pir = line.split(' -> ')
        pair_insertion_rules[pir[0]] = pir[1]


def chain_to_pairs(chain):
    pairs = {}
    for i in range(len(chain)-1):
        pair = chain[i:(i+2)]
        pairs[pair] = pairs.get(pair, 0) + 1
    return pairs

pairs = chain_to_pairs(chain)

def step_pairs(pairs):
    new_pairs = {}
    for pair, count in pairs.items():
        inserted = pair_insertion_rules[pair]
        new_pair1 = pair[0] + inserted
        new_pair2 = inserted + pair[1]
        new_pairs[new_pair1] = new_pairs.get(new_pair1, 0) + count
        new_pairs[new_pair2] = new_pairs.get(new_pair2, 0) + count
    return new_pairs


for steps in range(40):
    pairs = step_pairs(pairs)
    print(pairs)

element_count = {
    chain[-1]: 1,  # The last element will not be counted in the pair-loop below
}
for pair, count in pairs.items():
    # Only count 1st element (2nd element will be counted on the next pair)
    element_count[pair[0]] = element_count.get(pair[0], 0) + count

print(f"score: {max(element_count.values()) - min(element_count.values())}")
