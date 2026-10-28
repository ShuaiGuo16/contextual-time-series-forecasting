"""Create fictional meter readings from predeclared operating states.

The output is a synthetic tutorial fixture, not a measured building dataset.
No model output is used to set the readings.
"""
from pathlib import Path
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[1]
events = [('2026-08-20', 8, 18, 0, 0), ('2026-08-25', 18, 22, 2, 1), ('2026-08-29', 8, 12, 0, 1), ('2026-09-02', 12, 18, 2, 1), ('2026-09-07', 8, 12, 0, 0), ('2026-09-12', 12, 16, 1, 1), ('2026-09-17', 18, 22, 3, 1), ('2026-09-20', 0, 8, 0, 1), ('2026-09-23', 8, 18, 0, 0), ('2026-09-29', 12, 18, 1, 1), ('2026-10-03', 8, 12, 2, 1), ('2026-10-08', 18, 22, 1, 1), ('2026-10-13', 12, 18, 0, 0), ('2026-10-15', 18, 22, 2, 1), ('2026-10-17', 8, 12, 0, 1)]
rng = np.random.default_rng(42)
index = pd.date_range("2026-08-17", periods=63*24, freq="h")
weekday = index.dayofweek < 5
regular = weekday & (index.hour >= 8) & (index.hour < 18)
zones = np.where(regular, 4, 0)
vent = regular.astype(int)
for day, start, end, count, running in events:
    selected = (index >= pd.Timestamp(day) + pd.Timedelta(hours=start)) & (
        index < pd.Timestamp(day) + pd.Timedelta(hours=end))
    zones[selected] = count
    vent[selected] = running
day_number = np.arange(len(index)) // 24
daylight = np.clip(np.sin(np.pi * (index.hour.to_numpy()-6)/13), 0, None)
essential = 12 + 0.7*np.sin(2*np.pi*day_number/14)
zone_load = zones * (8.5 - 1.2*daylight)
fan_load = 13 * vent
daily_scale = rng.normal(1, 0.025, 63)[day_number]
readings = essential + daily_scale*(zone_load+fan_load) + rng.normal(0, 0.65, len(index))
pd.DataFrame({"timestamp":index, "kwh":readings.round(2)}).to_csv(root/"data/electricity.csv", index=False)
print(f"Prepared {len(index)} meter readings, 12 historical departures and 3 upcoming events.")
