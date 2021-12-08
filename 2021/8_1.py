import typing


displays = []
with open("8_1.input.txt", "r") as f:
    for line in f.readlines():
        segment_patterns, output = line.rstrip().split('|')
        segment_patterns = {
            frozenset(pattern)
            for pattern in segment_patterns.split()
        }
        output = [
            frozenset(pattern)
            for pattern in output.split()
        ]
        displays.append((segment_patterns, output))


def find_shuffled_font(characters: typing.Set[frozenset]) -> typing.Mapping[frozenset, int]:
    FONT = {
        0: frozenset('abcefg'),
        1: frozenset('cf'),
        2: frozenset('acdeg'),
        3: frozenset('acdfg'),
        4: frozenset('bcdf'),
        5: frozenset('abdfg'),
        6: frozenset('abdefg'),
        7: frozenset('acf'),
        8: frozenset('abcdefg'),
        9: frozenset('abcdfg'),
    }

    fwd = {}
    rev = {}
    # Easy ones first:
    for char in characters:
        if len(char) == 2:
            fwd[1] = char
            rev[char] = 1
        elif len(char) == 3:
            fwd[7] = char
            rev[char] = 7
        elif len(char) == 4:
            fwd[4] = char
            rev[char] = 4
        # len 5 ambiguous: 2, 3, 5
        # len 6 ambiguous: 0, 6, 9
        elif len(char) == 7:
            fwd[8] = char
            rev[char] = 8
    for char in fwd.values():
        characters.remove(char)

    # Now disambiguate the difficult ones
    # to identify: 2, 3, 5; 0, 6, 9
    for char in characters:
        if len(char) == 5:  # 2, 3, 5
            # `3` has the same digits as `1`, plus 3 more. 2 and 5 do not
            if char.intersection(fwd[1]) == fwd[1]:
                fwd[3] = char
                rev[char] = 3
        elif len(char) == 6:
            # `0` and `9` have the same digits as `1`, plus more. `6` does not
            if char.intersection(fwd[1]) != fwd[1]:
                fwd[6] = char
                rev[char] = 6
    for char in fwd.values():
        if char in characters:
            characters.remove(char)

    # to identify: 2, 5; 0, 9
    for char in characters:
        if len(char) == 5:
            # `5` is a subset of `6`, while `2` is not
            if fwd[6].intersection(char) == char:
                fwd[5] = char
                rev[char] = 5
            else:
                fwd[2] = char
                rev[char] = 2
        elif len(char) == 6:
            # `9` has the same digits as `3`, plus more. `0` does not
            if char.intersection(fwd[3]) == fwd[3]:
                fwd[9] = char
                rev[char] = 9
            else:
                fwd[0] = char
                rev[char] = 0
    for char in fwd.values():
        if char in characters:
            characters.remove(char)

    assert len(characters) == 0

    return rev


one_four_seven_eight_count = 0
for segment_patterns, output in displays:
    shuffeled_font = find_shuffled_font(segment_patterns)
    decoded_output = [
        shuffeled_font[digit]
        for digit in output
    ]

    print(''.join([str(_) for _ in decoded_output]))
    for digit in decoded_output:
        if digit in {1, 4, 7, 8}:
            one_four_seven_eight_count += 1

print(one_four_seven_eight_count)
