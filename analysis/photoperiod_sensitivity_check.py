python"""
Photoperiod Sensitivity Check: sigmoid vs. binary cutoff
==========================================================

Compares the photo factor output of a sigmoid transition function (k=0.5,
inflection=23.5°) against the binary |lat| ≥ 23.5° cutoff previously used
in the Ae. albopictus suitability model.

Outputs:
- Console summary: rows affected, unique cities, countries
- Edge-case table: cities at |lat| 20–30° with |delta| > 0.05
- Focus country table: Dengue analysis countries with |delta| > 0.1
- photoperiod_sensitivity.png: delta distribution and scatter by latitude

Input: mosquito_suitability.csv (city × month suitability scores)
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── 1. LOAD ──────────────────────────────────────────────────────────────────
df = pd.read_csv("mosquito_suitability.csv")
# Expected columns: city, country, lat, lon, month, suitability_score_albopictus

MONTHS_NORTH_WINTER = [11, 12, 1, 2]
MONTHS_SOUTH_WINTER = [5, 6, 7, 8]

# ── 2. BINARY PHOTO FACTOR (current logic) ───────────────────────────────────
def photo_factor_binary(lat, month, min_val=0.0):
    abs_lat = abs(lat)
    is_n_winter = (lat >= 0) and (month in MONTHS_NORTH_WINTER)
    is_s_winter = (lat < 0)  and (month in MONTHS_SOUTH_WINTER)
    if not (is_n_winter or is_s_winter):
        return 1.0
    return min_val if abs_lat >= 23.5 else 1.0

# ── 3. SIGMOID PHOTO FACTOR (new logic) ──────────────────────────────────────
def photo_factor_sigmoid(lat, month, k=0.5, inflection=23.5, min_val=0.0):
    abs_lat = abs(lat)
    is_n_winter = (lat >= 0) and (month in MONTHS_NORTH_WINTER)
    is_s_winter = (lat < 0)  and (month in MONTHS_SOUTH_WINTER)
    if not (is_n_winter or is_s_winter):
        return 1.0
    reduction = 1.0 / (1.0 + np.exp(-k * (abs_lat - inflection)))
    return round(1.0 - (1.0 - min_val) * reduction, 4)

# ── 4. APPLY BOTH ─────────────────────────────────────────────────────────────
df["photo_binary"]  = df.apply(lambda r: photo_factor_binary(r["lat"], r["month"]), axis=1)
df["photo_sigmoid"] = df.apply(lambda r: photo_factor_sigmoid(r["lat"], r["month"]), axis=1)
df["photo_delta"]   = (df["photo_sigmoid"] - df["photo_binary"]).round(4)

# ── 5. SUMMARY ────────────────────────────────────────────────────────────────
threshold = 0.1
affected = df[df["photo_delta"].abs() > threshold]

print(f"Total rows:              {len(df)}")
print(f"Rows with |delta| > {threshold}: {len(affected)}")
print(f"Unique cities affected:  {affected['city'].nunique()}")
print(f"Countries affected:      {affected['country'].nunique()}")
print()

# Cities near the boundary — the edge-case candidates
boundary_cities = df[
    (df["lat"].abs().between(20, 30)) &
    (df["photo_delta"].abs() > 0.05)
][["city", "country", "lat", "month", "photo_binary", "photo_sigmoid", "photo_delta"]]

print("── Edge-case cities (|lat| 20–30°, |delta| > 0.05) ──")
print(boundary_cities.sort_values("lat").to_string(index=False))

# ── 6. DENGUE FOCUS COUNTRIES ────────────────────────────────────────────────
focus = ["Taiwan", "Nicaragua", "Peru", "Mexico", "Colombia", "Singapore", "USA"]
focus_affected = affected[affected["country"].isin(focus)]

print(f"\n── Focus countries affected (|delta| > {threshold}) ──")
if focus_affected.empty:
    print("None — safe to proceed without fix.")
else:
    print(focus_affected[["city","country","lat","month","photo_delta"]]
          .sort_values(["country","lat"]).to_string(index=False))

# ── 7. PLOT ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: delta distribution
axes[0].hist(df["photo_delta"], bins=50, color="#3266ad", edgecolor="none", alpha=0.85)
axes[0].axvline(0, color="#888", linewidth=0.8, linestyle="--")
axes[0].axvline( threshold, color="#e07b39", linewidth=1, linestyle=":")
axes[0].axvline(-threshold, color="#e07b39", linewidth=1, linestyle=":")
axes[0].set_xlabel("Photo factor delta (sigmoid − binary)")
axes[0].set_ylabel("Row count")
axes[0].set_title("Distribution of delta across all city-months")

# Right: delta by latitude (winter months only)
winter_rows = df[df["photo_delta"] != 0]
axes[1].scatter(winter_rows["lat"], winter_rows["photo_delta"],
                alpha=0.3, s=8, color="#3266ad")
axes[1].axhline(0, color="#888", linewidth=0.8, linestyle="--")
axes[1].axhline( threshold, color="#e07b39", linewidth=1, linestyle=":")
axes[1].axhline(-threshold, color="#e07b39", linewidth=1, linestyle=":")
axes[1].axvline(23.5,  color="#3aaa6e", linewidth=1, linestyle=":")
axes[1].axvline(-23.5, color="#3aaa6e", linewidth=1, linestyle=":")
axes[1].set_xlabel("Latitude")
axes[1].set_ylabel("Photo factor delta")
axes[1].set_title("Delta by latitude (winter months only)")

plt.tight_layout()
plt.savefig("photoperiod_sensitivity.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nPlot saved: photoperiod_sensitivity.png")
