from __future__ import annotations
from pprint import pprint

from tools.graph import number_of_paths_between, dag_reverse

device_outputs = {}
with open("input.txt") as f:
    for line in f.read().splitlines():
        device, outputs = line.split(': ')
        device_outputs[device] = outputs.split(' ')
#pprint(device_outputs)

device_inputs = dag_reverse(device_outputs)


fft_dac_1 = number_of_paths_between(device_outputs, 'svr', 'fft', device_inputs)
fft_dac_2 = number_of_paths_between(device_outputs, 'fft', 'dac', device_inputs)
fft_dac_3 = number_of_paths_between(device_outputs, 'dac', 'out', device_inputs)
fft_dac = fft_dac_1 * fft_dac_2 * fft_dac_3
print(fft_dac_1, fft_dac_2, fft_dac_3, "=", fft_dac)

dac_fft_1 = number_of_paths_between(device_outputs, 'svr', 'dac', device_inputs)
dac_fft_2 = number_of_paths_between(device_outputs, 'dac', 'fft', device_inputs)
dac_fft_3 = number_of_paths_between(device_outputs, 'fft', 'out', device_inputs)
dac_fft = dac_fft_1 * dac_fft_2 * dac_fft_3
print(dac_fft_1, dac_fft_2, dac_fft_3, "=", dac_fft)

print(fft_dac + dac_fft)
