import dataclasses


@dataclasses.dataclass
class SpringRow:
    bitmap: str
    contiguous_groups: list[int]

    @staticmethod
    def bitmap_to_contiguous_groups(bitmap: str) -> list[int]:
        groups = []
        current_group = 0
        for i, ch in enumerate(bitmap):
            if ch == '#':
                current_group += 1
            elif ch == '.':
                if current_group > 0:
                    groups.append(current_group)
                    current_group = 0
        if current_group > 0:
            groups.append(current_group)
        return groups

    def possibilities(self) -> int:
        question_mark_idx = []
        for i, char in enumerate(self.bitmap):
            if char == '?':
                question_mark_idx.append(i)
        valid_possibilities = 0
        for possibility in range(2**len(question_mark_idx)):
            bitmap = list(self.bitmap)  # copy
            possibility_bits = format(possibility, f'0{len(question_mark_idx)}b')
            for bit_num, bit in enumerate(possibility_bits):
                bitmap[question_mark_idx[bit_num]] = '#' if bit == '1' else '.'
            possibility_groups = self.bitmap_to_contiguous_groups(bitmap)
            if possibility_groups == self.contiguous_groups:
                valid_possibilities += 1
        return valid_possibilities


spring_rows: list[SpringRow] = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        bitmap, cont_gr = line.split()
        cont_gr = [int(_) for _ in cont_gr.split(',')]
        spring_rows.append(SpringRow(bitmap, cont_gr))


total_possibilities = 0
for row in spring_rows:
    p = row.possibilities()
    print(f"{row}  =>  {p}")
    total_possibilities += p

print(total_possibilities)