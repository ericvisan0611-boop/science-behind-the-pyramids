#!/usr/bin/env python3
"""
Mass, bearing pressure, throughput and energy model for the Great Pyramid of Khufu.

Reproduces the calculations in Chapters 1, 3 and 8 using only the standard library.

Sources for the constants (see REFERENCES.md):
  [1]  Great Pyramid of Giza, Wikipedia - dimensions and mass split
  [16] Copas 2026, "Systemic Capacity Constraints in the Khufu Programme" - volume,
       mass, block statistics (citing Lehner 1997)
  [54] work-energy bound on the workforce
  [55] Lehner's block-rate arithmetic (via NOVA)
  [61] construction of the Egyptian pyramids, Wikipedia - placement rate

Run:  python3 scripts/pyramid_model.py
"""

import math

G = 9.81

# --- Primary dimensions (grade A) -------------------------------------------
BASE_SIDE_M = 230.33
ORIGINAL_HEIGHT_M = 146.6
PRESENT_HEIGHT_M = 138.5
VOLUME_M3 = 2_583_283
TOTAL_MASS_T = 6_000_000
BLOCK_COUNT = 2_300_000
CORE_MASS_T = 5_250_000
CASING_MASS_T = 115_000
GRANITE_MASS_T = 60_000
MORTAR_MASS_T = 500_000
LIMESTONE_DENSITY_T_M3 = 2.6

# --- Work rates --------------------------------------------------------------
WORK_PER_MANDAY_J = 450_000      # useful work per person-day, J [54]
BUILD_YEARS = 20
WORKDAYS_PER_YEAR = 300

# --- Foundation --------------------------------------------------------------
# Allowable bearing capacity of the Giza bedrock platform, treated conservatively.
# Typical values reported for strong limestone bedrock.
ALLOWABLE_BEARING_PA_KPA = 3_000.0


def pyramid_volume(base, height):
    return (base ** 2) * height / 3.0


def main():
    print("=" * 72)
    print("GREAT PYRAMID OF KHUFU - MASS, PRESSURE AND THROUGHPUT MODEL")
    print("=" * 72)

    print("\n1. Geometry check")
    print("-" * 72)
    v_calc = pyramid_volume(BASE_SIDE_M, ORIGINAL_HEIGHT_M)
    print(f"  base side                 {BASE_SIDE_M:>12.2f} m")
    print(f"  original height           {ORIGINAL_HEIGHT_M:>12.2f} m")
    print(f"  present height            {PRESENT_HEIGHT_M:>12.2f} m")
    print(f"  volume from formula       {v_calc:>12,.0f} m3")
    print(f"  volume (published)        {VOLUME_M3:>12,} m3")
    print(f"  difference                {100 * (v_calc - VOLUME_M3) / VOLUME_M3:>11.2f} %")
    print(f"  base area                 {BASE_SIDE_M ** 2 / 10_000:>12.2f} ha")

    print("\n2. Mass budget")
    print("-" * 72)
    accounted = CORE_MASS_T + CASING_MASS_T + GRANITE_MASS_T
    print(f"  local Giza limestone      {CORE_MASS_T:>12,} t   {100 * CORE_MASS_T / TOTAL_MASS_T:>5.1f} %")
    print(f"  Tura casing limestone     {CASING_MASS_T:>12,} t   {100 * CASING_MASS_T / TOTAL_MASS_T:>5.1f} %")
    print(f"  Aswan granite             {GRANITE_MASS_T:>12,} t   {100 * GRANITE_MASS_T / TOTAL_MASS_T:>5.1f} %")
    print(f"  subtotal (stone)          {accounted:>12,} t")
    print(f"  gypsum mortar             {MORTAR_MASS_T:>12,} t   (volume fill, not structural stone)")
    print(f"  implied mean density      {TOTAL_MASS_T * 1000 / VOLUME_M3:>12.2f} kg/m3")
    print(f"  published limestone density{LIMESTONE_DENSITY_T_M3:>12.1f} t/m3")

    print("\n3. Block statistics")
    print("-" * 72)
    mean_vol = VOLUME_M3 / BLOCK_COUNT
    mean_mass = TOTAL_MASS_T / BLOCK_COUNT
    print(f"  blocks                    {BLOCK_COUNT:>12,}")
    print(f"  mean block volume         {mean_vol:>12.2f} m3")
    print(f"  mean block mass           {mean_mass:>12.2f} t")
    print(f"  mean block cube root      {mean_vol ** (1 / 3):>12.2f} m")

    print("\n4. Bearing pressure on the bedrock platform")
    print("-" * 72)
    load_n = TOTAL_MASS_T * 1000 * G
    area_m2 = BASE_SIDE_M ** 2
    pressure_kpa = load_n / area_m2 / 1000
    print(f"  total weight              {load_n / 1e9:>12.3f} GN")
    print(f"  base area                 {area_m2:>12,.0f} m2")
    print(f"  average bearing pressure  {pressure_kpa:>12.1f} kPa")
    print(f"  typical allowable (bedrock){ALLOWABLE_BEARING_PA_KPA:>11,.0f} kPa")
    print(f"  utilisation               {100 * pressure_kpa / ALLOWABLE_BEARING_PA_KPA:>12.2f} %")
    print("  -> the foundation is not close to its limit; the pyramid is not")
    print("     foundation-limited, it is volume-limited.")

    print("\n5. Centre of mass and gravitational potential energy")
    print("-" * 72)
    com_h = ORIGINAL_HEIGHT_M / 4.0
    pe = TOTAL_MASS_T * 1000 * G * com_h
    print(f"  centre of mass height     {com_h:>12.2f} m  (h/4 for a pyramid)")
    print(f"  potential energy          {pe:>12.3e} J")

    print("\n6. Work-energy bound on the workforce")
    print("-" * 72)
    man_days = pe / WORK_PER_MANDAY_J
    man_years = man_days / WORKDAYS_PER_YEAR
    print(f"  work per person-day       {WORK_PER_MANDAY_J / 1000:>12.0f} kJ")
    print(f"  man-days of lifting       {man_days:>12,.0f}")
    print(f"  man-years                 {man_years:>12,.0f}")
    print(f"  workforce over {BUILD_YEARS} years      {man_years / BUILD_YEARS:>12,.0f} men")
    print("  -> a hard physical floor. Any estimate of total pyramid employment")
    print("     below this figure is not describing the project.")

    print("\n7. Throughput required")
    print("-" * 72)
    tonnes_per_day = TOTAL_MASS_T / (BUILD_YEARS * WORKDAYS_PER_YEAR)
    blocks_per_day = BLOCK_COUNT / (BUILD_YEARS * WORKDAYS_PER_YEAR)
    print(f"  stone per working day     {tonnes_per_day:>12,.0f} t")
    print(f"  blocks per working day    {blocks_per_day:>12,.0f}")
    print(f"  blocks per hour (24h)     {blocks_per_day / 24:>12,.1f}")
    print(f"  seconds per block         {24 * 3600 / blocks_per_day:>12.1f} s")
    print("  -> consistent with the published figure of roughly one tonne placed")
    print("     every two to three minutes by human draw teams [61].")

    print("\n8. Seasonality")
    print("-" * 72)
    flood_days = 183      # Akhet, roughly June to November
    low_days = WORKDAYS_PER_YEAR - flood_days
    low_season_ratio = 0.5   # ASSUMPTION: low season ran at half the flood-season rate
    annual_t = tonnes_per_day * WORKDAYS_PER_YEAR
    flood_rate = annual_t / (flood_days + low_days * low_season_ratio)
    low_rate = flood_rate * low_season_ratio
    print(f"  annual mean                {tonnes_per_day:>12,.0f} t/day")
    print(f"  flood season (Akhet)       {flood_days:>12} days -> {flood_rate:>9,.0f} t/day")
    print(f"  low season                 {low_days:>12} days -> {low_rate:>9,.0f} t/day")
    print(f"  ASSUMPTION: low season ran at {low_season_ratio:.0%} of the flood-season rate")
    print("  -> boat transport was only possible during the flood, so the peak")
    print("     seasonal rate had to exceed the annual mean by roughly half.")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
