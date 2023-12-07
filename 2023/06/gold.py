import dataclasses
import math

with open("input.txt", "r") as f:
    times = f.readline()
    _, times = times.split(':')
    times = [times.replace(' ', '')]

    distances = f.readline()
    _, distances = distances.split(':')
    distances = [distances.replace(' ', '')]


@dataclasses.dataclass
class Race:
    time_ms: int
    distance_mm: int

    @staticmethod
    def distance_for_time_pushed(time_pushed_ms: int, total_time_ms: int) -> int:
        speed_mm_per_ms = time_pushed_ms * 1  # 1mm/ms per 1ms of pushing
        time_remaining_ms = total_time_ms - time_pushed_ms
        distance_mm = time_remaining_ms * speed_mm_per_ms
        return distance_mm
        # distance_mm = (total_time_ms - time_pushed_ms) * (time_pushed_ms * 1)
        #             = total_time_ms * time_pushed_ms - time_pushed_ms ** 2

    @staticmethod
    def push_interval_to_win(total_time_ms: int, current_record: int) -> int:
        # d = -t^2 + TT*t

        # RD = record distance
        # -t^2 + TT*t - RD = 0   for what t's
        # t^2 - TT*t + RD = 0   for what t's
        # t = (-b ± sqrt(b^2 - 4ac)) / 2a
        # t > TT/2 ± 1/2*sqrt(TT^2 - 4*RD)

        best_time_ms = total_time_ms / 2
        #print(f"{best_time_ms=}")
        time_range_ms = math.sqrt(total_time_ms * total_time_ms - 4 * (current_record+1))  # +1 to make sure we win and not tie
        better_start = best_time_ms - time_range_ms / 2
        better_end = best_time_ms + time_range_ms / 2
        # print(f"up: {better_start} ({Race.distance_for_time_pushed(better_start, total_time_ms)}), "
        #       f"down: {better_end} ({Race.distance_for_time_pushed(better_end, total_time_ms)})")

        int_time_range = math.floor(better_end) - math.ceil(better_start) + 1
        #print(f"{int_time_range=}")
        return int_time_range



races = [Race(time_ms=int(_[0]), distance_mm=int(_[1])) for _ in zip(times, distances)]

product = 1
for race in races:
    possible_wins = Race.push_interval_to_win(total_time_ms=race.time_ms, current_record=race.distance_mm)
    product *= possible_wins

print(product)
