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

bag_contents = {
    'red': 12,
    'green': 13,
    'blue': 14,
}
game_sum = 0
for game_id, shows in games.items():
    possible = True
    for show in shows:
        for color, color_in_bag in bag_contents.items():
            if show.get(color, 0) > color_in_bag:
                possible = False

    #print(f"game {game_id}: {possible=}")

    if possible:
        game_sum += game_id

print(game_sum)
