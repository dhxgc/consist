import pandas as pd
import numpy as np
from scipy.signal import find_peaks

# Загрузка данных
df = pd.read_csv("power_grid.csv")
voltage = df["voltage"].values
time = df["time"].values

# 1. Определение частоты дискретизации
time_step = time[1] - time[0]
SAMPLING_RATE = int(1 / time_step)

# 2. Сглаживание данных
window_size = int(SAMPLING_RATE * 0.5)
smoothed = pd.Series(voltage).rolling(window_size, center=True).mean().values

# 3. Нахождение BIT_DURATION через автокорреляцию
correlation = np.correlate(smoothed - smoothed.mean(), 
                           smoothed - smoothed.mean(), mode='full')
peaks, _ = find_peaks(correlation, distance=SAMPLING_RATE)  # Игнорируем близкие пики
BIT_DURATION = (peaks[1] - peaks[0]) * time_step

# 4. Извлечение битов
samples_per_bit = int(BIT_DURATION * SAMPLING_RATE)
bits = []
for i in range(0, len(voltage), samples_per_bit):
    chunk = voltage[i:i+samples_per_bit]
    bits.append(1 if np.mean(chunk) > np.median(voltage) else 0)  # Медиана как порог

# 5. Байты → Флаг (little-endian)
flag_bytes = bytearray()
for i in range(0, len(bits), 8):
    byte_bits = bits[i:i+8]
    if len(byte_bits) < 8:
        break
    byte = sum(bit << idx for idx, bit in enumerate(byte_bits))
    flag_bytes.append(byte)

# Результат
try:
    print("Flag:", flag_bytes.decode())
except UnicodeDecodeError:
    print("HEX:", flag_bytes.hex())