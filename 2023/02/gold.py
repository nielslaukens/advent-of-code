games = {}

with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        game_id, shows = line.split(': ')
        game_id = int(game_id[5:])
        shows = shows.split('; ')
        cubes = []
        for show in shows:
            cube_list = show.split(', ')
            cube_dict = {}
            for cube_color in cube_list:
                num, color = cube_color.split(' ')
                cube_dict[color] = int(num)
            cubes.append(cube_dict)
        games[game_id] = cubes

power_sum = 0
for game_id, shows in games.items():
    min_color = {'red': 0, 'green': 0, 'blue': 0}
    for show in shows:
        for color, color_in_bag in min_color.items():
            if show.get(color, 0) > color_in_bag:
                min_color[color] = show[color]

    game_power = min_color['red'] * min_color['green'] * min_color['blue']
    print(f"game {game_id}: {game_power=}")
    power_sum += game_power

print(power_sum)
