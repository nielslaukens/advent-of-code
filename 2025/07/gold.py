with open("input.txt", "r") as f:
    lines = [
        list(_.rstrip())
        for _ in f.readlines()
    ]

start_column = lines[0].index('S')
beam_columns = {start_column: 1}
line = 1

timelines = 0
while line < len(lines):
    beams_out = {}
    for beam_column, timelines in beam_columns.items():
        material = lines[line][beam_column]
        if material == '.':
            beams_out[beam_column] = beams_out.get(beam_column, 0) + timelines
        elif material == '^':
            assert beam_column-1 >= 0
            assert beam_column+1 < len(lines[line])
            beams_out[beam_column-1] = beams_out.get(beam_column-1, 0) + timelines
            beams_out[beam_column+1] = beams_out.get(beam_column+1, 0) + timelines
    beam_columns = beams_out
    line += 1

print(sum(beam_columns.values()))
