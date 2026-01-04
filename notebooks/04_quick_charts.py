import pandas as pd
import matplotlib.pyplot as plt

dau = pd.read_csv("outputs/daily_dau.csv")
dau["event_date"] = pd.to_datetime(dau["event_date"])

plt.figure(figsize=(10,4))
plt.plot(dau["event_date"], dau["DAU"])
plt.title("Daily Active Users (DAU)")
plt.xlabel("Date")
plt.ylabel("DAU")
plt.tight_layout()
plt.savefig("outputs/dau_trend.png", dpi=200)
print("Saved outputs/dau_trend.png")
