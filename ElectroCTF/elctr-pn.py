import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("power_grid.csv")
plt.figure(figsize=(15, 4))
plt.plot(df["time"], df["voltage"], color="blue", linewidth=2)
plt.xlabel("Time (seconds)", fontsize=12)
plt.ylabel("Voltage (V)", fontsize=12)
plt.title("Power Grid Data (Clean Signal)", fontsize=14)
plt.ylim(200, 240)
plt.grid(True)
plt.savefig("power_plot.png", dpi=300)
plt.close()