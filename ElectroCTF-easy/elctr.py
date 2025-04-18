import pandas as pd
import numpy as np

FLAG = "el3ctr1ctf"
OUTPUT_CSV = "power_grid.csv"
BASE_VOLTAGE = 220.0
BIT_DURATION = 1  # 1 секунда на бит
SAMPLING_RATE = 10  # 10 точек в секунду

flag_bits = []
for char in FLAG:
    byte = ord(char)
    for i in range(8): 
        flag_bits.append((byte >> i) & 1)

total_time = len(flag_bits) * BIT_DURATION
time = np.round(np.arange(0, total_time, 1/SAMPLING_RATE), 1)
voltage = np.full(len(time), BASE_VOLTAGE)

for i, bit in enumerate(flag_bits):
    start = i * BIT_DURATION
    end = start + BIT_DURATION
    indices = np.where((time >= start) & (time < end))[0]
    voltage[indices] = 230 if bit else 210

pd.DataFrame({"time": time, "voltage": voltage}).to_csv(OUTPUT_CSV, index=False)