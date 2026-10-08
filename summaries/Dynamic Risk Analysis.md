# Kristensen, Liu & Utne 2022: Dynamic risk analysis of an autonomous surface ship

- **Paper:** Kristensen, Liu & Utne, "Dynamic Risk Analysis of Maritime Autonomous Surface Ships", PSAM16, 2022.
- **Link:** [PDF](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf) (open access)
- **Read:** all (12 pp). **Status:** read.
- **This summary:** "My notes (Jake)" are my own. Sections marked [Claude] were written by Claude from the full paper; check them against the paper before using them in the review.
- **Used in:** Intro · 2.3 DRA · Comparative analysis · Existing approaches & limitations · Identified gap · Positioning

**In one line:** a dynamic Bayesian network estimates, every 2 hours, the probability that a small USV's mission fails without a human stepping in. It's the closest prior work to ours.

## My notes (Jake)

risk assessment, considering power consumption vs situational awareness (SA) in marine autnomous surface ships (MASS) using a dynamic Bayesian belief network (DBN) model
- improved SA increases power consumption
- decreasing the level of autonomy (LOA) might *influence* the risk or SA
- the RA takes external factors and determines a probability of mission success/failure
  - determines the probability of mission being possibily **WITHOUT HUMAN INTERACTION**
  this is the big link to us, we are both determining porbability of the necessity of human interaction by external factors

their output is really P(a human has to step in)

> "can also give indications for when the human operator on shore should pay more attention"

-- same as us kinda

- We can get inspiration of their framework of calculating risk by external factors by using a bayesian network or a DBN.  Though different factors, similar idea. we also want to output a probability of necessity of human interaction.

Pros:
- in depth risk calculation

Cons:
- designed for a mission path

differences:
- uses wave-foil porpulsion

## [Claude] Summary

- **Goal:** dynamic risk analysis (DRA) of a MASS, focused on the trade-off between power and situational awareness (SA). Better SA needs more sensors and sampling, which drains the battery.
- **Method:** a dynamic Bayesian network (DBN).
  - Environmental inputs (wind speed, wave height, sun, temperature, current, obstacle density, comms coverage) and system inputs (battery level, energy use) feed middle nodes (available power, SA, propulsion).
  - Those feed three sub-tasks (collect data, follow path, avoid collision/grounding), which feed the end node, P(mission failure).
  - Inputs have coarse states (high/medium/low), and each time step is 2 h.
- **Where the probabilities come from:** system data, weather statistics, expert judgement, and some stated assumptions. Nothing is learned from logged outcomes.
- **Case study:** the AutoNaut, a 5 m USV with wave-foil propulsion and solar power for its electronics. The mission ran for 19 days in a defined area off Norway, with a shore operator checking in every 2 h. The real vessel grounded in a storm with a low battery after losing comms, and the model's risk rose to about 0.85 for the storm period.
- **Validation:** a sensitivity analysis on one input (sun exposure), plus a by-eye match to what happened on that one mission.
- **Intended use:** mission planning and operator decision support. The model "can also give indications for when the human operator on shore should pay more attention".

## [Claude] Strengths and weaknesses

**Strengths**
- **Handles time:** risk is updated at every step (the day/night cycle, the storm), which a static risk analysis can't do.
- **Probability output:** an alert threshold could be set on it.
- **Built around a human supervisor** with a 2 h check-in, close to OOR's pilot command every 2–3 h.

**Weaknesses**
- **Probabilities are not learned:** they come from experts and assumptions. Table 4 marks current strength, initial battery and energy consumption as "Assumption".
- **Hard to use as an alert as-is:** P(failure) sits around 0.6–0.7 for almost the whole mission (Fig. 3), so any threshold low enough to catch the storm would fire nearly all the time.
- **No wind direction:** only wind speed is an input. For us, direction relative to the station is one of the main signals.

## [Claude] How it relates to our paper

**The link:** both projects output a probability that a human has to step in, to support a shore operator. The difference is how that probability is produced (expert-set vs learned from telemetry) and what it's about (mission failure from power/SA vs position near the 10 nm boundary).

| Section | How to use it |
|---|---|
| Abstract / 1. Introduction | This paper is why "none of these methods explore… *when* human interaction is needed" has to be narrowed: the idea exists here. |
| 2.3 DRA | The representative *dynamic*, expert-based risk model. Contrast it with Na 2025 (static, qualitative). |
| Hierarchy figure | Risk & supervision × physics/expert-based. |
| Comparative analysis: table (Rowan) | One row; see the table below. |
| Comparative analysis: Venn (Rowan) | Circle C (risk). It's the closest to the centre, since it's a USV with a human operator. |
| Existing approaches & limitations (Rowan) | Its weakness is *not* "relies on oceanographic models" (that fits Dugan and Song). It's expert-set probabilities validated on one mission. |
| Identified gap (Rowan) | Narrow the gap to what's missing: learned from telemetry, about position/boundary risk, and validated against real pilot interventions. |
| Positioning (Rowan) | Work we *build on*: the same output idea, but learned and position-based. |

> Optional idea: a BN fits your plan better than it might look. Their high/medium/low states look a lot like your V1 grid's bands, and learning a node's probability table from logged interventions is basically your V2 "per-cell frequencies" step. That's a positioning point: the same structure idea, but with probabilities learned from data instead of set by experts.

## [Claude] Compared with our project

| | Kristensen et al. 2022 | Our project |
|---|---|---|
| Vessel | AutoNaut: 5 m, wave-foil propulsion, solar for electronics, max 2 kn | OOR DataXplorer |
| Mission | 19 days in a defined area off Norway, collecting data | Ongoing station keeping within 10 nm of Station 46012 |
| What goes wrong | Power runs low, so SA, data collection and navigation degrade | Wind pushes the vessel toward the 10 nm limit |
| Output | P(mission failure without manual intervention) at each 2 h step | P(pilot must intervene within Δt), e.g. Δt = 1 h |
| Inputs | Sun, temperature, waves, wind speed, current, obstacles, comms coverage, battery | Position, distance to station, wind speed and direction |
| Probabilities from | Experts, weather statistics, assumptions | V1: pilot rules; V2: learned from simulation and logged interventions |
| Run on | Evidence set by hand from the forecast and mission plan | Live telemetry |
| Validation | One mission, sensitivity analysis | Recall, false alerts per shift, watch hours removed, against the V1 grid |
| Human role | Shore operator checks every 2 h; the model supports planning | Pilot moves from 24/7 watch to on-call alerts |

## [Claude] To fix in the background doc

- "Identified Gap in the Literature" says the literature "lacks a clear integration between dynamic risk scoring and automated human-intervention triggers". This paper proposes that link, so narrow the claim.
