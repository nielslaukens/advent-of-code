with open("10.input.txt", "r") as f:
    lines = [
        line.strip()
        for line in f.readlines()
    ]

matching_pairs = {
    '[': ']',
    '{': '}',
    '(': ')',
    '<': '>',
}
score_table = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

score = 0
for linenum, line in enumerate(lines):
    state = ''
    for charnum, char in enumerate(line):
        if char in matching_pairs.keys():
            state += char
        elif char in matching_pairs.values():
            expected_close = matching_pairs[state[-1]]
            if char == expected_close:
                state = state[:-1]
            else:
                print(f"Line {linenum}: syntax error at position {charnum}: "
                      f"expected {expected_close} but got {char}")
                score += score_table[char]
                break
    if state != '':
        print(f"Line {linenum}: incomplete, still open: {state}")
    else:
        print(f"Line {linenum}: OK")

print(f"Syntax error score: {score}")
