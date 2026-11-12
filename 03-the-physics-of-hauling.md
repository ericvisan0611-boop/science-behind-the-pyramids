# 03 — The Physics of Hauling

This is the chapter that dissolves the central "impossible" claim. Every number here is either measured in a laboratory, measured on site, or measured in a documented replication experiment.

## Friction, defined

For a block dragged across a surface, the force needed to keep it moving is the normal force (its weight component pressing into the surface) multiplied by a dimensionless coefficient of sliding friction, μ_d:

```
F_friction = μ_d · m · g
```

Everything else in this chapter is about reducing μ_d, or about not fighting friction at all.

For a 2.5-tonne block (m ≈ 2500 kg, weight ≈ 24.5 kN), the difference between plausible coefficients is the difference between a few dozen men and a few hundred:

| Condition | μ_d | Force on a 2.5 t block | Implied crew (at ~500 N per sustained puller) |
|---|---|---|---|
| Stone dragged on dry sand | 0.6–0.8 (static) | 14.7–19.6 kN | 30–40 pullers just to start it |
| Wooden sledge on wet sand | 0.2–0.3 | 4.9–7.4 kN | 10–15 pullers |
| Wooden rollers on a prepared road | 0.05–0.1 | 1.2–2.5 kN | 3–5 pullers |

Static and kinetic friction figures for these configurations, and the crew sizes they imply, are assembled in the transport-analysis literature on Old Kingdom stone movement [29]. The row that matters most is the middle one, because it is the row the Egyptians are documented to have used.

## Wet sand: the capillary bridge effect

The tomb of Djehutihotep at el-Bersheh, dating to the Twelfth Dynasty around 1880 BCE, shows a colossus of roughly 60–80 t on a sledge hauled by 172 men on four ropes, with one man standing in front of the sledge pouring water onto the sand [31][13]. This painting has been read for two thousand years as an exotic flourish. In 2014 it became a physics paper.

Daniel Bonn and colleagues at the University of Amsterdam published *Sliding friction on wet and dry sand* in *Physical Review Letters* [31]. The finding is precise and counterintuitive:

- Adding a small amount of water **greatly reduces** the sliding friction of an object dragged over sand — the coefficient decreases by almost a factor of two [31].
- The force needed to move a given load can be reduced by as much as **40%**, and by up to **70%** on standard sand [31].
- The effect is not monotonic. Above roughly **5% water content** the friction coefficient starts climbing again, and past about 7% wet sand has *more* friction than dry sand [31].

The mechanism is not lubrication in the oil sense. It is a change in the mechanical behaviour of the granular medium. In a three-phase sand–water–air system, water forms **capillary bridges** between adjacent grains. Those bridges generate capillary attraction and act as glue, raising the shear modulus of the sand mixture — the same effect that lets a sandcastle hold its shape [31]. A stiffer surface cannot be ploughed. The dry sledge digs a heap in front of itself and must drag that heap along; the wet sledge rides on a surface stiff enough that no heap forms, so the ploughing component of resistance disappears [31].

This is why the optimum is so narrow and why it is so useful. The Egyptians did not need a lubricant; they needed a **sandcastle**, and they had to add water in the right quantity. The mapping-ignorance summary of the paper puts the practical detail well: the optimum water fraction is close to 5%, the peak is sharp, and "for slightly more or less water volume fraction the friction coefficient rapidly increases" [32].

One of the paper's authors is blunt about the archaeological payoff: pouring a limited amount of water in front of a sledge greatly reduces the manpower necessary to transport a statue [33]. The paper's own discussion notes that the effect "seemed to be known by the ancient Egyptians," citing the Djehutihotep depiction [33].

**What this does not license.** The painting is Middle Kingdom, roughly a thousand years after Khufu [31]. The physical principle is universal; the specific practice is documented for one dynasty, not for the Great Pyramid. The gap is small — the mechanism is a property of sand — but it should be stated rather than smoothed over.

## The lubricant hierarchy: sand, tafla, gypsum

Mark Lehner, who ran the NOVA replication experiments, reports that thin *tafla* layers — calcareous desert clay — have been found under multi-ton blocks left in place at temple and monument walls, or set down en route by workers awaiting placement [34]. In the NOVA experiment, the team built a hauling track of wooden beams, sand and limestone debris, coated it with a thin layer of tafla, and had workers pull a two-ton limestone block on a wooden sledge while one worker wetted the clay ahead of the runners. The slick clay acted as a lubricant and greatly facilitated the pull [34].

Lehner's proposed hierarchy is a graded system rather than a single trick [34]:

- **Sand with water** for long, coarse movements over distance.
- **Tafla** for shorter, more precise movements and adjustments.
- **Gypsum mortar**, finer than tafla, for the most precise work — setting the outer casing stones [34].

That is a materials-selection argument, and it is the kind of thing that a logistics organisation produces when it has done the work many times and knows where its tolerances bind.

## Replication experiments

**Lehner and Hopkins, 1997 (NOVA).** Over a three-week build of an approximately 10 m pyramid [34][35]:

- Four or five men could use levers on stones under one ton to flip them and move them by rolling; larger stones had to be towed [35].
- Wooden sledges on wooden tracks let **12 to 20 men** tow a **two-tonne** stone [35].
- A 2.5 t block could be quarried with copper chisels and dolerite pounders in roughly 45 minutes [13].

**Parry and colleagues.** A 2.5 t block of 0.8 × 0.8 × 1.6 m was moved 80 m on level ground using 160 m of rope, and up a **1-in-4 slope** — steeper than the 1:12 or 1:8 grades actually attested at some pyramid sites — using wooden quarter-circle "cradle runners" or rockers that turn the square prism into a cylinder. The block could be rolled at a fast walking pace by two or three men pushing from behind, moved up the 1:4 slope by ten men, and taken up a 15 m ramp by fourteen, with twenty used more routinely. The implied coefficient of friction on a prepared roadway is about **μ_d = 0.2** [36].

**West and colleagues (Indiana University).** Their approach reduces ground pressure rather than friction: attach twelve wooden rods to the block so the square prism becomes a dodecagon, then pull a rope wrapped over the top. Measured dynamic friction coefficient in steady rolling, **μ_d ≈ 0.30 ± 0.05**, but the rope-over-block arrangement acts as a 2:1 pulley, so the force required is only **μ_d·m·g / 2 ≈ 0.15·m·g** [37][37]. The cost is that the rods must be about 30 cm in diameter — comparable to ship masts on the Nile — and the crew must be rotated continuously to compensate for the 2:1 crew-to-block distance disparity [37]. About 50 fit men would be needed to move 2,500 kg at 0.5 m/s [37].

Note what West's paper actually demonstrates: the rolling coefficient (0.30) is *worse* than Parry's sledge result (0.2), but the rope geometry halves the required pull. The two innovations are independent and multiply.

## Sledge versus roller: a genuine trade-off

Rollers are more efficient than sledges — rolling resistance of 0.05–0.1 on a prepared road against 0.2–0.3 for a wet-sand sledge [29]. But rollers have a hard constraint: **they are useless on sand.** They sink and fail to rotate, so rollers require a paved road [29]. At Giza that means constructing and maintaining a surfaced causeway of the kind described in [Chapter 2](02-logistics-and-waterways.md) — the same infrastructure the Widan el-Faras road represents [27][28].

At 3 tonnes, a sledge on wet sand needs roughly 600–900 kgf of pull; a block on rollers over a prepared surface needs only 150–300 kgf [29]. A single crew of sixteen workers can therefore move a 3 t block on rollers, and a workforce of about 500 can sustain 500 blocks per day on a single route at 1.3-minute intervals [29].

So the choice is not "sledges or rollers" as an abstract. It is:

- **Over sand, away from the road:** sledge, wetted, at μ_d ≈ 0.2–0.3. This is the documented practice, and the Djehutihotep painting is the record of it.
- **On a built road:** rollers, at μ_d ≈ 0.05–0.1, with a far higher setup cost in infrastructure and timber.
- **In close quarters, over short distances:** levers. Four or five men can lever and roll a block under a ton [35]; Herodotus's informants said blocks were moved by machines and levers [38]; the *shadoof*, a counterweighted lever used for irrigation, is documented in Egypt from the Old Kingdom period onward and is the obvious ancestor of any lever-based lifting scheme [38].

## Turning corners, and the geometry problem

A sledge-hauling operation has a worse problem than friction: it has a **corner problem**. A 2.5 t block on a 2 m sledge needs a turning radius it cannot easily achieve inside a ramp.

Lehner's NOVA team built a wrap-around ramp for their small pyramid and tried to turn a 3 t block around a corner by planting posts and pivoting the ropes against them. It "failed miserably": after getting the block two feet high the whole setup became wobbly and difficult to manage [38].

That is a small-scale failure of a small-scale experiment, and it should not be over-read — but it identifies exactly why the corner-notches in Houdin's reconstruction are a load-bearing part of his proposal rather than a decorative detail (see [Chapter 4](04-ramps-and-raising-blocks.md)).

## The energy floor

There is an independent way to bound the workforce, and it is worth doing because it bypasses every archaeological assumption about rates and shifts.

The gravitational potential energy of the pyramid is the mass raised against the height of its own centre of mass, which for a pyramid sits at one quarter of its height above the base:

```
E = m · g · h/4  ≈ 6.0e6 t · 9.81 m/s² · 36.65 m ≈ 2.16e12 J
```

At roughly 450 kJ of useful work per person-day — the physiological figure used in this line of argument — that implies roughly **5.3 million man-days**, about 18,000 man-years, and, spread over a 20-year build, a workforce of roughly **800-900 men** at the theoretical limit [39].

The real figure must be larger, because this counts only the work of lifting and ignores quarrying, hauling over friction, ramp construction, food preparation, surveying and everything else. Adding those, the same analysis lands on a grand total of construction labour of roughly **3,300 workers** [39]. Independent archaeological estimates converge on a comparable order: Lehner's own arithmetic gives 5,000 men or fewer for the building and quarrying work [40]; Tyldesley's synthesis gives about 4,000 primary labourers supported by 16,000–20,000 secondary workers [41]; the Digital Giza project puts the total at 20,000–30,000 [42]; Hawass argues for 36,000 [40].

The gap between the physical floor and the archaeological estimates is not a contradiction. The floor is a lower bound on *construction* labour; the estimates include the food chain, the port, the administration, the settlement and the seasonal labour levy — and the two ends of that range are answering slightly different questions. [Chapter 8](08-workforce-and-organisation.md) takes this apart properly.

## What the physics does and does not deliver

The physics closes the *haulage* problem decisively. A 2.5 t block on a wetted sand sledge needs roughly 10–20 men and about 100–200 kgf of pull [29][35]. That is a number of people you can find in a village.

The physics does not close the *lifting* problem. Raising a block to 140 m requires work against gravity that no coefficient of friction reduces. It is dealt with separately, in [Chapter 4](04-ramps-and-raising-blocks.md), where the honest answer turns out to be that this remains open.

---

**Next:** [04 — Ramps and Raising Blocks](04-ramps-and-raising-blocks.md)
