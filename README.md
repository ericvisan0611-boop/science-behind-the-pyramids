# The Science Behind the Pyramids

A research-grade, evidence-graded explainer of the engineering, physics, materials science, logistics, astronomy and modern measurement technology behind the Old Kingdom Egyptian pyramids.

The Great Pyramid of Khufu is treated as the primary case study because it is the only pyramid for which we have survey-grade metrology, a peer-reviewed physics literature, a directly excavated workforce settlement, and a continuous logbook written by the people who moved its stone.

**What this repository argues:** the pyramids are not an unsolved mystery of lost knowledge. They are a well-documented industrial and structural-engineering programme whose surviving open questions are narrow, specific, and nameable — and whose tools to close most of them already exist.

---

## The argument in one page

An "impossible" building is usually a chain of individually ordinary capabilities that nobody has connected. Six of them do most of the work here.

**1. Logistics before lifting.** The pyramid is 2.3 million blocks and roughly 6 million tonnes. But 83–92% of that mass is local Giza plateau limestone quarried on site. Only ~115,000 tonnes of Tura white limestone came by boat, and only tens of thousands of tonnes of Aswan granite. This is not a "ship 6 million tonnes" problem; it is a "move 300,000 tonnes a few dozen kilometres" problem. The expedition leader Merer kept a logbook of it ([Chapter 2](02-logistics-and-waterways.md)).

**2. Wet sand halves the friction.** The tomb painting of Djehutihotep shows a man pouring water in front of a sledge. In 2014, physicists at the University of Amsterdam measured why: a few per cent of water creates capillary bridges between sand grains, stiffening the surface so the sledge stops ploughing a heap. The friction coefficient roughly halves; the pulling force to start a given load drops by up to 40%, and by up to 70% on standard sand. Too much water and friction climbs back above dry. ([Chapter 3](03-the-physics-of-hauling.md))

**3. The pyramid's voids are structural, not decorative.** The Grand Gallery is corbelled to 1.0 m wide at the top and roofed with slabs laid at a *steeper* angle than the floor, each engaging a slot — so load goes into the walls instead of stacking onto the block below. Above the King's Chamber sit five relieving chambers that divert the superincumbent mass around the burial chamber. These are load paths, and they are the clearest evidence of genuine structural thinking in the building. ([Chapter 5](05-structural-engineering-inside.md))

**4. The frequency mismatch is measured.** Ambient-noise seismic surveying at 37 points inside and around the pyramid finds a fundamental frequency of 2.0–2.6 Hz inside the masonry against ~0.6 Hz in the surrounding soil. Resonance amplification therefore does not build up, which is a quantitative explanation for survival across the 1847 and 1992 earthquakes. The authors explicitly decline to claim the builders engineered this deliberately. ([Chapter 6](06-seismic-performance.md))

**5. Alignment is a metrology problem, not a mystery.** The 2015 resurvey of the base found 84 points of original casing baseline and put the west side at 4′21″ west of true north (95% CI 3′45″–4′56″). Several candidate techniques — pole star, circumpolar star pair, simultaneous stellar transit, equinoctial solar gnomon — have been field-tested and shown capable of comparable accuracy. The method is underdetermined; the precision is not. ([Chapter 7](07-surveying-and-astronomy.md))

**6. The frontier is non-destructive physics.** Cosmic-ray muon radiography found a 30-metre void above the Grand Gallery in 2017; a second corridor behind the north face chevron was found the same way in 2023 and finally seen with a 5 mm endoscope. Both have since been confirmed by ground-penetrating radar, ultrasonics and electrical resistivity tomography. The Big Void has still never been entered. ([Chapter 9](09-modern-measurement-science.md))

What remains genuinely open is narrower than the popular framing suggests: the *geometry of the ramps* above the lower courses, the *mechanism for raising blocks* in the upper third, the *function* of the two confirmed voids, and the *scale of the workforce*. Each has a named method that would settle it.

---

## Contents

| Chapter | Subject | What it settles |
|---|---|---|
| [01](01-materials-and-geology.md) | Materials and geology | Where every stone came from, what the tools could do, and how the core differs from the casing |
| [02](02-logistics-and-waterways.md) | Logistics and waterways | The Nile-to-plateau supply chain, Merer's logbook, the Ahramat Nile Branch |
| [03](03-the-physics-of-hauling.md) | The physics of hauling | Friction coefficients, wet sand, sledge vs. roller vs. rod, measured force budgets |
| [04](04-ramps-and-raising-blocks.md) | Ramps and raising blocks | The competing ramp models, their material cost, and their failure modes |
| [05](05-structural-engineering-inside.md) | Internal structural engineering | The Grand Gallery, the relieving chambers, the King's Chamber roof, the granite plugs |
| [06](06-seismic-performance.md) | Seismic performance | Ambient-noise surveying, frequency mismatch, historic earthquakes |
| [07](07-surveying-and-astronomy.md) | Surveying and astronomy | Alignment precision in arcminutes, candidate techniques, base levelling |
| [08](08-workforce-and-organisation.md) | Workforce and organisation | How many people, fed how, organised how, treated how |
| [09](09-modern-measurement-science.md) | Modern measurement science | Muography, the Big Void, the North Face Corridor, the 2026 frontier |
| [10](10-evidence-grading-and-open-questions.md) | Evidence grading | Every claim tagged A–E; the named open questions and what would close them |
| [11](11-contested-hypotheses.md) | Contested hypotheses | Pyramid-as-power-plant, pyramid-as-concrete, and why they are not equally serious |

Supporting material:

- [`data/pyramid_facts.csv`](data/pyramid_facts.csv) — every quantitative constant used in the chapters, one row per fact, with its source.
- [`data/alignment.csv`](data/alignment.csv) — measured alignment errors for the three great pyramids, in arcminutes.
- [`scripts/haul_model.py`](scripts/haul_model.py) — reproduces the friction and hauling-force calculations from [Chapter 3](03-the-physics-of-hauling.md).
- [`scripts/pyramid_model.py`](scripts/pyramid_model.py) — mass, base pressure and throughput model for the Great Pyramid.
- [`scripts/make_figures.py`](scripts/make_figures.py) — regenerates every figure in `figures/` from `data/`.
- [`REFERENCES.md`](REFERENCES.md) — the full bibliography, keyed by number and referenced inline throughout.

---

## Evidence grading

Every substantive claim in the chapters carries a grade. The scale is about *evidentiary strength*, not about how interesting a claim is.

| Grade | Meaning |
|---|---|
| **A** | Direct measurement or peer-reviewed finding, independently replicated or derived from primary data |
| **B** | Peer-reviewed model or interpretation that is not yet confirmed by independent observation |
| **C** | Scholarly inference from primary archaeological data, with the reasoning stated and checkable |
| **D** | Falsifiable hypothesis that is live in the literature but currently unsupported by direct evidence |
| **E** | Speculative or pseudo-scientific claim that is contradicted by the evidence, or not testable as stated |

The grading is applied honestly, including to claims that are dramatic. The Big Void is **A** as an existence claim and **D** as a functional claim. Houdin's internal ramp is **B**. The energy-machine hypothesis is **E**. Putting these on one visible scale is the single most useful editorial decision in this repository.

---

## Running the models

```bash
git clone https://github.com/ericvisan0611-boop/science-behind-the-pyramids.git
cd science-behind-the-pyramids

# Core physics and logistics model — prints a table, writes a CSV
python3 scripts/haul_model.py

# Mass, bearing pressure and daily throughput
python3 scripts/pyramid_model.py

# Regenerate all figures into figures/
pip install matplotlib
python3 scripts/make_figures.py
```

Only the standard library is required for the two model scripts. `make_figures.py` additionally requires `matplotlib`.

Figures are committed as SVG so they stay sharp at any size and remain diffable as text. `make_figures.py` writes both SVG and PNG versions; the PNGs are regenerated locally and are not tracked.

---

## Figures

| Figure | Shows |
|---|---|
| `figures/friction_vs_water.svg` | Sliding friction coefficient against water content — the wet-sand optimum |
| `figures/mass_breakdown.svg` | Where the 6 million tonnes came from |
| `figures/haul_force.svg` | Pulling force versus block mass for each transport method |
| `figures/alignment_errors.svg` | Measured alignment error of the three great pyramids, in arcminutes |
| `figures/seismic_spectrum.svg` | Fundamental frequency inside the pyramid vs. surrounding soil |
| `figures/structural_section.svg` | Schematic section of the internal chamber system |

---

## Conventions

- **Lengths** are metric unless quoted otherwise. `m³` is cubic metres, `t` is metric tonnes.
- **Alignment errors** are in arcminutes; 1° = 60′, 1′ = 60″. A negative value denotes a counterclockwise rotation from true north.
- **Friction coefficients** are dimensionless dynamic coefficients of sliding friction unless stated otherwise.
- **Dates** for ancient events are BCE; dates for modern research carry the year.
- **Quotations** from the Egyptian record are translated, and the source is named inline.
- Where sources conflict, both figures are given with their sources rather than silently averaged.

---

## A note on what this repository is not

It is not a debunking document. Several genuinely interesting hypotheses — internal ramps, in-situ construction sequences, the role of the Trial Passages — are described with the strongest case that can be made for them, along with what would count against them.

It is also not a mystery. There is no chapter explaining what the pyramids cannot explain, because there is very little they cannot explain once the logistics, the friction physics, the surveying and the labour organisation are laid out quantitatively.

And it is not finished. The open questions in [Chapter 10](10-evidence-grading-and-open-questions.md) are named, and for each one there is a measurement that would settle it. Several of those measurements are already scheduled.

---

## Licence

Content is released under the [MIT Licence](LICENSE). Source data in `data/` and code in `scripts/` carry the same licence. Published measurements remain the property of their original publishers and authors and are cited, not copied.
