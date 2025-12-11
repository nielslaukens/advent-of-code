from __future__ import annotations
from pprint import pprint

from tools.graph import topological_sort_dag

device_outputs = {}
with open("input.txt") as f:
    for line in f.read().splitlines():
        device, outputs = line.split(': ')
        device_outputs[device] = outputs.split(' ')
#pprint(device_outputs)

device_inputs = {}
for input, outputs in device_outputs.items():
    for output in outputs:
        device_inputs.setdefault(output, []).append(input)
pprint(device_inputs)

def number_of_paths_between(begin: str, end: str) -> int:
    num_paths: dict[str, int] = {}
    for f, ts in device_outputs.items():
        num_paths[f] = 0
        for t in ts:
            num_paths[t] = 0
    num_paths[end] = 1

    for node in topological_sort_dag(device_inputs):
        for next_node in device_outputs.get(node, []):
            num_paths[node] += num_paths[next_node]

    return num_paths[begin]

fft_dac_1 = number_of_paths_between('svr', 'fft')
fft_dac_2 = number_of_paths_between('fft', 'dac')
fft_dac_3 = number_of_paths_between('dac', 'out')
fft_dac = fft_dac_1 * fft_dac_2 * fft_dac_3
print(fft_dac_1, fft_dac_2, fft_dac_3, "=", fft_dac)

dac_fft_1 = number_of_paths_between('svr', 'dac')
dac_fft_2 = number_of_paths_between('dac', 'fft')
dac_fft_3 = number_of_paths_between('fft', 'out')
dac_fft = dac_fft_1 * dac_fft_2 * dac_fft_3
print(dac_fft_1, dac_fft_2, dac_fft_3, "=", dac_fft)

print(fft_dac + dac_fft)
