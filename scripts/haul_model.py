#!/usr/bin/env python3
"""
Haulage force model for Old Kingdom stone transport.

Reproduces the calculations in Chapter 3 of the repository using only the
standard library.

Sources for the constants (see REFERENCES.md):
  [39] obelisks.org transport analysis - static and rolling friction coefficients
  [42] Fall et al., Physical Review Letters 112, 175502 (2014) - wet sand
  [46] Lehner & Hopkins 1997 NOVA replication - crew sizes
  [47] Parry et al. - prepared roadway coefficient and 1:4 slope haul
  [48] West et al. - rod-dodecagon rolling method
  [54] work-energy bound on the workforce

Run:  python3 scripts/haul_model.py
"""

import math

G = 9.81          # m/s^2
PULLER_FORCE_N = 500.0   # sustained pull per fit worker, N (order-of-magnitude physiology)

# Friction coefficients, dimensionless dynamic unless noted.
MU_SAND_STATIC = (0.60, 0.80)   # [39] stone on dry sand, static
MU_SLEDGE_WET = (0.20, 0.30)     # [39] wooden sledge on wet sand, kinetic
MU_ROLLER_ROAD = (0.05, 0.10)    # [39] wooden rollers on a prepared road
MU_ROD_ROLLING = 0.30           # [48] rod-dodecagon, steady rolling
ROD_MECH_ADVANTAGE = 2.0        # [48] rope wrapped over the block
MU_PREPARED_ROAD = 0.20         # [47] Parry, full-scale block on cradle runners


def wet_sand_mu(water_fraction, mu_dry=0.60, mu_opt=0.32, w_opt=0.05, w_crossover=0.07):
    """
    Interpolating model of the sliding friction coefficient of a sledge over
    sand as a function of water volume fraction.

    Anchored to the measured behaviour reported by Fall et al. (2014):
      - friction falls by almost a factor of two from dry to optimum
      - the minimum sits close to 5% water content
      - above ~5% friction rises again
      - past ~7% wet sand has MORE friction than dry sand

    This is a smooth curve through the published endpoints, not a fit to the
    original measurements; it is intended for illustration, not for prediction.
    """
    w = max(0.0, water_fraction)
    if w <= w_opt:
        # Cosine interpolation from dry down to the optimum.
        t = w / w_opt
        return mu_dry + (mu_opt - mu_dry) * (1.0 - math.cos(math.pi * t)) / 2.0
    if w <= w_crossover:
        # Between the optimum and the crossover, friction climbs back to dry.
        t = (w - w_opt) / (w_crossover - w_opt)
        return mu_opt + (mu_dry - mu_opt) * t ** 2
    # Beyond the crossover, wet sand is worse than dry sand.
    t = min(1.0, (w - w_crossover) / (0.20 - w_crossover))
    return mu_dry + (mu_dry - mu_opt) * t


def pulling_force(mass_kg, mu, gradient_deg=0.0):
    """Force required to haul a sledge/roller load up a ramp at a given gradient."""
    theta = math.radians(gradient_deg)
    normal = mass_kg * G * math.cos(theta)
    along = mass_kg * G * math.sin(theta)
    return mu * normal + along


def crew_size(force_n):
    """Number of sustained pullers needed to supply a given force."""
    return math.ceil(force_n / PULLER_FORCE_N)


def main():
    print("=" * 72)
    print("HAULAGE FORCE MODEL")
    print("=" * 72)

    print("\n1. Sliding friction vs water content (Fall et al. 2014 behaviour)")
    print("-" * 72)
    print(f"{'water %':>8}  {'mu_d':>6}  {'pull on 2.5 t':>15}  {'crew':>5}")
    for w_pct in (0, 1, 2, 3, 4, 5, 6, 7, 8, 10):
        mu = wet_sand_mu(w_pct / 100.0)
        f = pulling_force(2500.0, mu)
        print(f"{w_pct:>8}  {mu:>6.3f}  {f / 1000:>12.2f} kN  {crew_size(f):>5}")

    print("\n2. Methods compared on level ground and on a 7 degree ramp")
    print("-" * 72)
    methods = [
        ("Stone on dry sand (static)", MU_SAND_STATIC[1], 1.0),
        ("Sledge on wet sand (optimally wetted)", wet_sand_mu(0.05), 1.0),
        ("Sledge on wet sand (over-wetted)", wet_sand_mu(0.09), 1.0),
        ("Rollers on prepared road", MU_ROLLER_ROAD[1], 1.0),
        ("Rod-dodecagon, 2:1 rope advantage", MU_ROD_ROLLING / ROD_MECH_ADVANTAGE, 1.0),
    ]
    header = f"{'method':<42}{'mu_eff':>8}{'flat 2.5t':>13}{'crew':>6}{'7deg 2.5t':>13}{'crew':>6}"
    print(header)
    for name, mu, _ in methods:
        f_flat = pulling_force(2500.0, mu)
        f_ramp = pulling_force(2500.0, mu, 7.0)
        print(f"{name:<42}{mu:>8.3f}{f_flat / 1000:>10.2f} kN{crew_size(f_flat):>6}"
              f"{f_ramp / 1000:>10.2f} kN{crew_size(f_ramp):>6}")

    print("\n3. Crew size vs block mass, sledge on wet sand (mu = 0.25)")
    print("-" * 72)
    print(f"{'mass (t)':>10}{'flat kN':>10}{'crew':>6}{'7deg kN':>10}{'crew':>6}"
          f"{'11.3deg kN':>12}{'crew':>6}")
    for mass_t in (0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 60.0, 80.0):
        m = mass_t * 1000.0
        f0 = pulling_force(m, 0.25)
        f1 = pulling_force(m, 0.25, 7.0)
        f2 = pulling_force(m, 0.25, 11.3)
        print(f"{mass_t:>10.1f}{f0 / 1000:>10.2f}{crew_size(f0):>6}"
              f"{f1 / 1000:>10.2f}{crew_size(f1):>6}{f2 / 1000:>12.2f}{crew_size(f2):>6}")

    print("\n4. The Hatnub ramp, the steepest measured Old Kingdom haul ramp")
    print("-" * 72)
    mu = 0.25
    for mass_t in (2.5, 5.0, 20.0):
        m = mass_t * 1000.0
        f = pulling_force(m, mu, 11.3)
        print(f"  {mass_t:>5.1f} t block at 20% gradient: {f / 1000:>6.2f} kN "
              f"-> {crew_size(f):>3} pullers")
    print("  (Parry et al. moved a 2.5 t block up a 1:4 slope with 10-14 men [47])")

    print("\n5. Rod-dodecagon method: the 2:1 advantage")
    print("-" * 72)
    for mass_t in (2.5, 5.0, 10.0):
        m = mass_t * 1000.0
        raw = MU_ROD_ROLLING * m * G
        effective = raw / ROD_MECH_ADVANTAGE
        print(f"  {mass_t:>5.1f} t: raw rolling resistance {raw / 1000:>6.2f} kN "
              f"-> effective {effective / 1000:>6.2f} kN -> {crew_size(effective):>3} pullers")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
