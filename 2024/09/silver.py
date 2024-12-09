disk_map: list = []
with open("input.txt", "r") as f:
    state = 'file'
    file_id = 0
    for l in f.readline().strip():
        l = int(l)
        if state == 'file':
            disk_map.extend([file_id] * l)
            file_id += 1
            state = 'free'
        elif state == 'free':
            disk_map.extend([None] * l)
            state = 'file'
        else:
            raise RuntimeError(f"Unknown state {state}")

print(disk_map)

# Optimize search:
nothing_free_before = 0
nothing_in_use_after = len(disk_map) - 1


def find_free_location():
    global nothing_free_before
    while disk_map[nothing_free_before] is not None:
        nothing_free_before += 1
    return nothing_free_before


def find_last_in_use_block():
    global nothing_in_use_after
    while disk_map[nothing_in_use_after] is None:
        nothing_in_use_after -= 1
    return nothing_in_use_after


while True:
    free_location = find_free_location()
    in_use_block = find_last_in_use_block()
    if free_location >= in_use_block:
        break
    disk_map[free_location], disk_map[in_use_block] = disk_map[in_use_block], disk_map[free_location]  # swap
print(disk_map)

checksum = 0
for pos, file_id in enumerate(disk_map):
    if file_id is None:
        pass
    else:
        checksum += pos * file_id

print(f"checksum: {checksum}")
