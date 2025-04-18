import pandas as pd
import numpy as np

df = pd.read_csv("power_grid.csv")
voltage = df["voltage"].values

samples_per_bit = 30  # SAMPLING_RATE * BIT_DURATION

bits = []
for i in range(0, len(voltage), samples_per_bit):
    chunk = voltage[i:i+samples_per_bit]
    bits.append(1 if np.mean(chunk) > 220 else 0)

flag_bytes = bytearray()
for i in range(0, len(bits), 8):
    byte_bits = bits[i:i+8]
    if len(byte_bits) < 8:
        break
    byte = 0
    for idx, bit in enumerate(byte_bits):
        byte |= bit << idx 
    flag_bytes.append(byte)

try:
    flag = flag_bytes.decode("utf-8")
    print("Flag:", flag)
except UnicodeDecodeError:
    print("Ошибка декодирования. HEX флага:", flag_bytes.hex())