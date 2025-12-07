with open("input.txt", "r") as f:
    lines = [
        list(_.rstrip())
        for _ in f.readlines()
    ]

start_column = lines[0].index('S')
beam_columns = {start_column}
line = 1

num_splits = 0
while line < len(lines):
    beams_out = set()
    for beam_column in beam_columns:
        material = lines[line][beam_column]
        if material == '.':
            beams_out.add(beam_column)
        elif material == '^':
            assert beam_column-1 >= 0
            assert beam_column+1 < len(lines[line])
            beams_out.add(beam_column-1)
            beams_out.add(beam_column+1)
            num_splits += 1
    beam_columns = beams_out
    line += 1

print(num_splits)
