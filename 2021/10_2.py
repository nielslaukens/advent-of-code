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
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

score = []
for linenum, line in enumerate(lines):
    state = ''
    try:
        for charnum, char in enumerate(line):
            if char in matching_pairs.keys():
                state += char
            elif char in matching_pairs.values():
                expected_close = matching_pairs[state[-1]]
                if char == expected_close:
                    state = state[:-1]
                else:
                    raise SyntaxError(f"Line {linenum}: syntax error at position {charnum}: "
                          f"expected {expected_close} but got {char}")

        if state != '':  # incomplete line
            completion_string = ''.join([
                matching_pairs[open_char]
                for open_char in reversed(state)
            ])
            line_score = 0
            for char in completion_string:
                line_score = line_score * 5 + score_table[char]
            print(f"Line {linenum}: score {line_score}")
            score.append(line_score)

    except SyntaxError:
        pass  # ignore corrupt lines

print(f"Autocomplete score: {sorted(score)[len(score)//2]}")
