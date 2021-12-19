"""
Not optimized enough.
Current runtime for sample: 1.85s
Current runtime for input: 3m39s
"""

import typing

import numpy


def read_input(fn: str):
    with open(fn, "r") as f:
        lines = [
            line.strip()
            for line in f.readlines()
        ]
    scanner_data = []
    this_scanner_data = None
    for line in lines:
        if line.startswith('--- scanner '):
            this_scanner_data = []
        elif line == '':
            scanner_data.append(this_scanner_data)
        else:
            x, y, z = line.split(',')
            this_scanner_data.append([int(x), int(y), int(z)])
    if len(this_scanner_data):
        scanner_data.append(this_scanner_data)
    return scanner_data


scanner_data = read_input("19.input.txt")

scanner_data = [
    numpy.array(single_scanner_data)
    for single_scanner_data in scanner_data
]

ORIENTATIONS = [
    'xyz', 'y-xz', '-x-yz', '-yxz',  # z<=z
    '-zyx', 'yzx', 'z-yx', '-y-zx',  # x<=z
    'x-zy', '-z-xy', '-xzy', 'zxy',  # y<=z
    '-xy-z', '-y-x-z', 'x-y-z', 'yx-z',  # -z<=z
    'zy-x', '-yz-x', '-z-y-x', 'y-z-x',  # -x<=z
    'xz-y', '-zx-y', '-x-z-y', 'z-x-y',  # -y<=z
]
for i in range(len(ORIENTATIONS)):
    o = ORIENTATIONS[i]
    a = []
    sign = 1
    for c in o:
        if c == '-':
            sign = -1
        elif c == 'x':
            a.append(numpy.array([1, 0, 0]) * sign)
            sign = 1
        elif c == 'y':
            a.append(numpy.array([0, 1, 0]) * sign)
            sign = 1
        elif c == 'z':
            a.append(numpy.array([0, 0, 1]) * sign)
            sign = 1
        else:
            RuntimeError()
    ORIENTATIONS[i] = numpy.stack(a)
    assert numpy.linalg.det(ORIENTATIONS[i]) == 1  # we didn't accidentally make a left-handed axis

# p = numpy.array([5, 6, 7])
# for o in ORIENTATIONS:
#     print(numpy.matmul(o, p))


def ndarray_to_set_of_tuple(a: numpy.ndarray) -> typing.Set[typing.Tuple[int, int, int]]:
    s = set()
    for el_num in range(a.shape[0]):
        s.add((a[el_num, 0], a[el_num, 1], a[el_num, 2]))
    return s


def num_matching_beacons(
        a: typing.Set[typing.Tuple[int, int, int]],
        b: numpy.ndarray,
) -> int:
    """
    Calculate number of matching beacons.
    Assumes both are in the same coordinate system.
    """
    b_set = ndarray_to_set_of_tuple(b)
    both = a.intersection(b_set)
    return len(both)


def match_beacons_translate_only(
        sensor_a_beacons: typing.Set[typing.Tuple[int, int, int]],
        sensor_b_beacons: numpy.ndarray,
        min_matching: int,
) -> typing.Optional[numpy.ndarray]:
    """
    Search for matching beacons between `sensor_a_beacons` and `sensor_b_beacons`,
    assuming their orientation matches.
    Returns either the offset of sensor_b relative to sensor_a,
    or None if no 12 matching beacons were found.
    """
    # naive approach: full search
    for beacon_a in sensor_a_beacons:
        for beacon_b_num in range(sensor_b_beacons.shape[0]):
            # assume sensor_a_beacons[beacon_a_num] is the same beacon as
            # sensor_b_beacons[beacon_b_num]
            sensor_b_relative_to_sensor_a = beacon_a - sensor_b_beacons[beacon_b_num]
            sensor_b_beacons_relative_to_sensor_a = sensor_b_beacons + sensor_b_relative_to_sensor_a
            m = num_matching_beacons(sensor_a_beacons, sensor_b_beacons_relative_to_sensor_a)
            if m >= min_matching:
                return sensor_b_relative_to_sensor_a
    return None


def match_beacons(
        sensor_a_beacons: typing.Set[typing.Tuple[int, int, int]],
        sensor_b_beacons: numpy.ndarray,
        min_matching: int,
) -> typing.Optional[typing.Tuple[numpy.ndarray, numpy.ndarray]]:
    """
    Search for matching beacons between `sensor_a_beacons` and `sensor_b_beacons`..
    Returns either a tuple:
      - offset of sensor_b relative to sensor_a
      - rotation of sensor_b relative to sensor_a
    or None if no 12 matching beacons were found.
    """
    for orientation in ORIENTATIONS:
        rotated_sensor_b_beacons = (orientation.reshape(1, 3, 3) @ sensor_b_beacons.reshape(-1, 3, 1)).reshape(-1, 3)
        translation = match_beacons_translate_only(
            sensor_a_beacons,
            rotated_sensor_b_beacons,
            min_matching,
        )
        if translation is not None:
            return translation, orientation
    return None


def test():
    # simple translation b is at (-1, -1, -1)
    a = numpy.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    b = numpy.array([[1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2]])
    t, r = match_beacons(ndarray_to_set_of_tuple(a), b, 4)
    assert (t == numpy.array([-1, -1, -1])).all()
    assert (r == ORIENTATIONS[0]).all()
    b_ = (r.reshape(1, 3, 3) @ b.reshape(-1, 3, 1)).reshape(-1, 3) + t
    assert (b_ == a).all()

    # simple rotation b is rotated 180º around the x axis
    a = numpy.array([[0, 0, 0], [1, 0, 0], [0, 2, 0], [0, 0, 3]])
    b = numpy.array([[0, 0, 0], [1, 0, 0], [0, -2, 0], [0, 0, -3]])
    t, r = match_beacons(ndarray_to_set_of_tuple(a), b, 4)
    assert (t == numpy.array([0, 0, 0])).all()
    assert (r == numpy.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])).all()
    b_ = (r.reshape(1, 3, 3) @ b.reshape(-1, 3, 1)).reshape(-1, 3) + t
    assert (b_ == a).all()

    # b is at (-1, -1, -1) and rotated 180º around the x-axis
    a = numpy.array([[0, 0, 0], [1, 0, 0], [0, 2, 0], [0, 0, 3]])
    b = numpy.array([[1, -1, -1], [2, -1, -1], [1, -3, -1], [1, -1, -4]])
    t, r = match_beacons(ndarray_to_set_of_tuple(a), b, 4)
    assert (t == numpy.array([-1, -1, -1])).all()
    assert (r == numpy.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])).all()
    b_ = (r.reshape(1, 3, 3) @ b.reshape(-1, 3, 1)).reshape(-1, 3) + t
    assert (b_ == a).all()
test()


sensors_to_position = set(range(len(scanner_data)))
sensors_to_position.remove(0)  # sensor 0 is our reference, at position (0, 0, 0) and oriented "correctly"
global_map = ndarray_to_set_of_tuple(scanner_data[0])

while len(sensors_to_position):
    for sensor_to_position in sensors_to_position:
        m = match_beacons(global_map, scanner_data[sensor_to_position], min_matching=12)
        if m is None:
            continue
        t, r = m
        print(f"Matched sensor {sensor_to_position}. Is at {t}, oriented {r}")
        new_beacons = (r.reshape(1, 3, 3) @ scanner_data[sensor_to_position].reshape(-1, 3, 1)).reshape(-1, 3) + t
        global_map = global_map.union(ndarray_to_set_of_tuple(new_beacons))
        break

    else:  # no break in loop
        raise RuntimeError(f"Could not position any more sensors. Remaining: {sensors_to_position}")
    if sensor_to_position is not None:
        sensors_to_position.remove(sensor_to_position)

print(f"Found {len(global_map)} sensors")
