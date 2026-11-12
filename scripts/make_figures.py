#!/usr/bin/env python3
"""
Regenerate every figure in figures/ from data/.

Requires matplotlib.  Run:  python3 scripts/make_figures.py
"""

import csv
import math
import os
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    sys.exit("matplotlib is required: pip install matplotlib")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
FIGS = os.path.join(ROOT, "figures")

INK = "#1c1c1c"
ACCENT = "#9a6b2f"
ACCENT2 = "#3f6b8a"
MUTED = "#b9b2a4"
GRID = "#e2ddd2"


def style():
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "figure.dpi": 150,
    })


def read_facts():
    path = os.path.join(DATA, "pyramid_facts.csv")
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[row["id"]] = row
    return out


def fact(facts, pid):
    return float(facts[pid]["value"].split("-")[0])


# --------------------------------------------------------------------------


def fig_friction(facts):
    """Sliding friction coefficient against water content."""
    sys.path.insert(0, HERE)
    from haul_model import wet_sand_mu

    ws = [i / 20.0 for i in range(0, 201)]
    mus = [wet_sand_mu(w) for w in ws]

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.plot([w * 100 for w in ws], mus, color=ACCENT, linewidth=2.4)
    ax.axvline(5, color=ACCENT2, linestyle="--", linewidth=1.2)
    ax.annotate("optimum ~5%\nwater", xy=(5, min(mus)),
                xytext=(7.2, min(mus) + 0.14), color=ACCENT2, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=ACCENT2, lw=1.1))
    ax.axvline(7, color=MUTED, linestyle=":", linewidth=1.2)
    ax.annotate("friction exceeds\ndry sand beyond ~7%", xy=(7, 0.6),
                xytext=(10.5, 0.5), color=INK, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.set_xlabel("Water content (% of sand volume)")
    ax.set_ylabel("Sliding friction coefficient")
    ax.set_title("Wet sand halves the friction of a dragged sledge")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 0.78)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "friction_vs_water.svg"))
    fig.savefig(os.path.join(FIGS, "friction_vs_water.png"))
    plt.close(fig)


def fig_mass(facts):
    """Where the six million tonnes came from."""
    labels = ["Local Giza\nlimestone\n(core)", "Tura white\nlimestone\n(casing)",
              "Aswan\ngranite\n(chambers)", "Gypsum\nmortar"]
    values = [fact(facts, "P08"), fact(facts, "P09"),
              fact(facts, "P10"), fact(facts, "P11")]
    colors = [ACCENT, ACCENT2, "#6b5b45", MUTED]

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    left = 0.0
    for label, value, color in zip(labels, values, colors):
        ax.barh([0], [value / 1000.0], left=left, color=color, height=0.42, label=label)
        if value / TOTAL_M3 > 400:
            ax.text(left + value / 2000.0, 0, f"{value:,.0f} t",
                    ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        left += value / 1000.0

    ax.set_xlabel("Thousand tonnes")
    ax.set_title("Most of the pyramid never left the Giza plateau")
    ax.set_yticks([])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=4, frameon=False, fontsize=9)
    ax.set_xlim(0, left * 1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "mass_breakdown.svg"))
    fig.savefig(os.path.join(FIGS, "mass_breakdown.png"))
    plt.close(fig)


TOTAL_M3 = 5500.0


def fig_haul_force(facts):
    """Pulling force versus block mass for each transport method."""
    masses = [0.5, 1, 2.5, 5, 10, 25, 60, 80]
    methods = [
        ("Stone on dry sand (static)", 0.80, MUTED, "--"),
        ("Sledge on wet sand", 0.25, ACCENT, "-"),
        ("Rollers on prepared road", 0.10, ACCENT2, "-"),
        ("Rod-dodecagon (2:1 rope)", 0.15, "#6b5b45", ":"),
    ]
    g = 9.81
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for name, mu, color, ls in methods:
        y = [mu * m * 1000 * g / 1000.0 for m in masses]
        ax.plot(masses, y, marker="o", color=color, linestyle=ls, linewidth=2.0, label=name)
    ax.set_xlabel("Block mass (tonnes)")
    ax.set_ylabel("Pulling force (kN)")
    ax.set_title("Hauling force scales with mass and with the method")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(frameon=False, fontsize=9)
    ax.annotate("a 2.5 t block on a wetted sledge:\nabout 6 kN, 13 pullers",
                xy=(2.5, 6.1), xytext=(4.2, 1.1), fontsize=9, color=ACCENT,
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.1))
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "haul_force.svg"))
    fig.savefig(os.path.join(FIGS, "haul_force.png"))
    plt.close(fig)


def fig_alignment(facts):
    """Measured alignment errors in arcminutes."""
    path = os.path.join(DATA, "alignment.csv")
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)

    keep = [r for r in rows
            if "Mean of three" not in r["pyramid"] and "Trial" not in r["pyramid"]]
    names = [r["pyramid"] for r in keep]
    values = [float(r["alignment_error_arcmin"]) for r in keep]
    colors = []
    for r in keep:
        if "Experimental" in r["pyramid"]:
            colors.append(ACCENT2)
        elif "Trial" in r["pyramid"]:
            colors.append(MUTED)
        else:
            colors.append(ACCENT)

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ypos = range(len(names))
    ax.barh(list(ypos), values, color=colors, height=0.6)
    ax.set_yticks(list(ypos))
    ax.set_yticklabels([n.replace(", ", ",\n") for n in names], fontsize=9)
    ax.axvline(0, color=INK, linewidth=1.0)
    ax.set_xlabel("Alignment error (arcminutes from true north; negative = counterclockwise)")
    ax.set_title("Every great pyramid is rotated slightly counterclockwise")
    ax.text(0.99, 0.02, "Trial Passages (+15') omitted: a survey-feature offset, not a pyramid error",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#6b6459")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "alignment_errors.svg"))
    fig.savefig(os.path.join(FIGS, "alignment_errors.png"))
    plt.close(fig)


def fig_seismic(facts):
    """Fundamental frequency inside the pyramid vs the surrounding soil."""
    soil = 0.6
    lo, hi = 2.0, 2.6
    mean = 2.3

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.barh([1], [hi - lo], left=lo, color=ACCENT, height=0.42,
            label="Pyramid masonry: 2.0-2.6 Hz (mean 2.3)")
    ax.axvline(mean, color=INK, linewidth=1.4)
    ax.barh([0], [0.18], left=soil - 0.09, color=ACCENT2, height=0.42,
            label="Surrounding soil: ~0.6 Hz")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Soil", "Pyramid"])
    ax.set_xlabel("Fundamental frequency (Hz)")
    ax.set_title("The frequency mismatch that prevents resonance")
    ax.set_xlim(0, 3.2)
    ax.annotate("no shared resonance\nmode", xy=(1.45, 0.5), fontsize=9, color=INK,
                ha="center")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "seismic_spectrum.svg"))
    fig.savefig(os.path.join(FIGS, "seismic_spectrum.png"))
    plt.close(fig)


def fig_section(facts):
    """Schematic section of the internal chamber system."""
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    h = 146.6
    base = 230.3

    ax.plot([0, base / 2, base, 0], [0, h, 0, 0], color=MUTED, linewidth=1.2,
            linestyle="--", zorder=1)

    def rect(x0, y0, w, hgt, face, edge=INK):
        ax.add_patch(plt.Rectangle((x0, y0), w, hgt, facecolor=face,
                                   edgecolor=edge, linewidth=0.9, zorder=3))

    cx = base / 2

    # Relieving chambers (five), lowest first
    for i in range(5):
        rect(cx - 13, 49 + i * 4.4, 26, 3.2, "#efe6d4")
    # King's Chamber and its roof slabs
    rect(cx - 13, 43, 26, 5.2, "#e8d9c0")
    # Queen's Chamber
    rect(cx - 6, 22, 12, 5.5, "#e8d9c0")

    # Ascending passage / Grand Gallery (sloping) and the King's Chamber shafts.
    # Drawn up into the clear space above the chambers so the labels never
    # overlap the masonry.
    ax.plot([cx - 2.4, cx - 2.4], [27.5, 100], color=ACCENT, linewidth=1.7, zorder=2)
    ax.plot([cx + 2.4, cx + 2.4], [27.5, 100], color=ACCENT2, linewidth=1.7, zorder=2)
    ax.plot([cx, cx], [0, 15], color="#6b5b45", linewidth=1.4, linestyle=":", zorder=2)

    def callout(x_text, y_text, text, xy, color=INK, ha="left", fs=8):
        ax.annotate(text, xy=xy, xytext=(x_text, y_text), fontsize=fs, color=color,
                    ha=ha, va="center", zorder=5,
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.9,
                                    shrinkA=0, shrinkB=2))

    callout(20, 88, "Five relieving chambers\ndivert load around the chamber",
            (cx - 13, 64), fs=8.5)
    callout(20, 45.5, "King's Chamber\ngranite, 9 roof slabs", (cx - 13, 45.5), fs=8.5)
    callout(20, 24.5, "Queen's Chamber", (cx - 6, 24.5), fs=8.5)
    callout(150, 34, "Subterranean Chamber\ncut in bedrock, unfinished", (cx, 14), fs=8.5)
    ax.text(cx + 16.0, 90, "Ascending passage / Grand Gallery", fontsize=8.5,
            color=ACCENT, rotation=90, va="center", ha="center")
    ax.text(cx - 16.0, 90, "King's Chamber shafts", fontsize=8.5,
            color=ACCENT2, rotation=90, va="center", ha="center")

    ax.set_xlim(0, base)
    ax.set_ylim(-6, h + 10)
    ax.set_aspect("equal")
    ax.set_xlabel("Base (230.3 m)")
    ax.set_ylabel("Height above base (m)")
    ax.set_title("Internal chamber system and load paths")
    ax.grid(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "structural_section.svg"))
    fig.savefig(os.path.join(FIGS, "structural_section.png"))
    plt.close(fig)


def main():
    os.makedirs(FIGS, exist_ok=True)
    style()
    facts = read_facts()
    fig_friction(facts)
    fig_mass(facts)
    fig_haul_force(facts)
    fig_alignment(facts)
    fig_seismic(facts)
    fig_section(facts)
    print("Figures written to:", FIGS)
    for name in sorted(os.listdir(FIGS)):
        if name.endswith((".png", ".svg")):
            path = os.path.join(FIGS, name)
            print(f"  {name:<32} {os.path.getsize(path):>8,} bytes")


if __name__ == "__main__":
    main()
