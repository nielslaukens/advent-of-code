import typing


class BitCount:
    def __init__(self):
        self.count_false = 0
        self.count_true = 0

    def add(self, bit: bool) -> None:
        if bit:
            self.add_true()
        else:
            self.add_false()

    def add_true(self) -> None:
        self.count_true += 1

    def add_false(self) -> None:
        self.count_false += 1

    def most_common(self) -> typing.Optional[bool]:
        if self.count_true > self.count_false:
            return True
        elif self.count_false > self.count_true:
            return False
        else:
            return None

    def least_common(self) -> typing.Optional[bool]:
        most_common = self.most_common()
        if most_common is None:
            return None
        return not most_common


diag_report = []
with open("3_1.input.txt", "r") as f:
    for line in f.readlines():
        bits = list(line.rstrip())
        diag_report.append([
            bit == '1'
            for bit in bits
        ])

num_bits = len(diag_report[0])


def filter_list_per_bit(
        full_list: typing.List[typing.List[bool]],
        most_common: bool = True,
        ex_aequo: bool = True
) -> typing.List[bool]:
    filtered_list = full_list
    for i in range(0, num_bits):
        bit_count = BitCount()
        for diag_entry in filtered_list:
            bit_count.add(diag_entry[i])

        if most_common:
            value_to_keep = bit_count.most_common()
        else:
            value_to_keep = bit_count.least_common()
        if value_to_keep is None:
            value_to_keep = ex_aequo
        filtered_list = [
            entry
            for entry in filtered_list
            if entry[i] == value_to_keep
        ]
        if len(filtered_list) == 1:
            return filtered_list[0]
    raise ValueError("Filter left >1 entry")


def bool_list_to_int(bool_list: typing.List[bool]) -> int:
    bits = ''.join(['1' if _ else '0' for _ in bool_list])
    return int(bits, 2)


oxygen_generator_rate = bool_list_to_int(filter_list_per_bit(
    diag_report,
    most_common=True,
    ex_aequo=True,
))
print(f"oxygen generator rate = {oxygen_generator_rate}")

co2_scrubber_rate = bool_list_to_int(filter_list_per_bit(
    diag_report,
    most_common=False,
    ex_aequo=False,
))
print(f"co2 scrubber rate = {co2_scrubber_rate}")

print(f"product: {oxygen_generator_rate * co2_scrubber_rate}")
