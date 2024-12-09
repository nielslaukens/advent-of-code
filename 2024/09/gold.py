import dataclasses


@dataclasses.dataclass
class File:
    file_id: int | None  # none: free
    length: int
    already_moved: bool = False

    def __repr__(self) -> str:
        file_id = self.file_id
        if file_id is None:
            file_id = '.'
        else:
            file_id = str(file_id)
        return f"{file_id}×{self.length}"


compressed_disk_map: list = []
with open("input.txt", "r") as f:
    state = 'file'
    file_id = 0
    for l in f.readline().strip():
        l = int(l)
        if state == 'file':
            f = File(file_id, l)
            file_id += 1
            state = 'free'
        elif state == 'free':
            f = File(None, l)
            state = 'file'
        else:
            raise RuntimeError(f"Unknown state {state}")
        compressed_disk_map.append(f)

print(compressed_disk_map)


def move_file_to_free_space(location_of_file: int, location_of_free_space: int) -> tuple[int, int]:
    global compressed_disk_map
    assert location_of_file > location_of_free_space
    file = compressed_disk_map[location_of_file]
    free_space = compressed_disk_map[location_of_free_space]
    new_disk_fragment_instead_of_free_space = [
        file,
        File(None, free_space.length - file.length),
    ]
    new_disk_fragment_instead_of_file = [
        File(None, file.length),
    ]
    compressed_disk_map = [
        *compressed_disk_map[0:location_of_free_space],  # everything before free space
        *new_disk_fragment_instead_of_free_space,
        *compressed_disk_map[location_of_free_space+1:location_of_file],  # between free space and file
        *new_disk_fragment_instead_of_file,
        *compressed_disk_map[location_of_file+1:],
    ]
    location_of_file, location_of_free_space = location_of_free_space, location_of_file+1
    # location_of_file + 1 because we split the free space up into 2 parts (of possible 0-length)

    # now defragment free space
    new_compressed_disk_map = []
    for old_idx, stretch in enumerate(compressed_disk_map):
        new_idx = len(new_compressed_disk_map)

        if len(new_compressed_disk_map) > 0:
            if new_compressed_disk_map[-1].file_id == stretch.file_id:
                # combine into previous segment
                assert new_compressed_disk_map[-1].file_id is None
                new_compressed_disk_map[-1].length += stretch.length
                stretch.length = 0
        if stretch.length == 0:
            pass  # swallow 0-length segments
        else:
            new_compressed_disk_map.append(stretch)

        if old_idx == location_of_file:
            location_of_file = new_idx
        if old_idx == location_of_free_space:
            location_of_free_space = new_idx

    compressed_disk_map = new_compressed_disk_map

    return location_of_file, location_of_free_space


location_to_relocate = len(compressed_disk_map) - 1

while location_to_relocate > 0:
    print(location_to_relocate)

    file = compressed_disk_map[location_to_relocate]
    if file.file_id is None or file.already_moved:
        location_to_relocate -= 1
        continue

    # scan for free space large enough
    free_space_location = None
    for stretch_location, stretch in enumerate(compressed_disk_map):
        if (stretch.file_id is None  # free space
                and stretch.length >= file.length  # large enough
        ):
            free_space_location = stretch_location
            break
    if free_space_location is not None and free_space_location < location_to_relocate:
        #print(f"moving file_id {file.file_id} to free space at {free_space_location}")
        file.already_moved = True
        _, location_to_relocate = move_file_to_free_space(location_to_relocate, free_space_location)
        #print(compressed_disk_map)
    else:
        pass  # print(f"not moving file_id {file.file_id}, no free space")

    location_to_relocate -= 1

checksum = 0
p = 0
for stretch in compressed_disk_map:
    for i in range(stretch.length):
        if stretch.file_id is not None:
            checksum += p * stretch.file_id
        p += 1
print(f"Checksum: {checksum}")
