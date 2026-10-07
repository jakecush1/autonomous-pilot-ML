> | 1 | **Kristensen, Liu & Utne 2022**, "Dynamic Risk Analysis of Maritime Autonomous Surface Ships", PSAM16. [PDF](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf) | Closest prior work: risk model for a USV with a shore operator checking in every 2 h; suggests the model can tell the operator when to pay attention | **All** (12 pp) | 2.3, comparison, positioning |

risk assessment, considering power consumption vs situational awareness (SA) in marine autnomous surface ships (MASS) using a dynamic Bayesian belief network (DBN) model
- improved SA increases power consumption
- decreasing the level of autonomy (LOA) might *influence* the risk or SA
- the RA takes external factors and determines a probability of mission success/failure
  - determines the probability of mission being possibily **WITHOUT HUMAN INTERACTION**
  this is the big link to us, we are both determining porbability of the necessity of human interaction by external factors

their output is really P(a human has to step in)

- **Goal:** dynamic risk analysis (DRA) of a MASS, focused on the trade-off between power and situational awareness (SA). Better SA needs more sensors and sampling, which drains the battery.

- **Method:** a dynamic Bayesian network (DBN). Environmental inputs (wind speed, wave height, sun, temperature, current, obstacle density, comms coverage) and system inputs (battery level, energy use) feed middle nodes (available power, SA, propulsion). These feed three sub-tasks (collect data, follow path, avoid collision/grounding), which feed the end node, P(mission failure). Inputs have coarse states (high/medium/low), and each time step is 2 h.

- **Where the probabilities come from:** system data, weather statistics, expert judgement, and some stated assumptions. Nothing is learned from logged outcomes.

- **Case study:** the AutoNaut, a 5 m USV with wave-foil propulsion and solar power for its electronics. The mission ran 19 days in a defined area off Norway, with a shore operator checking in every 2 h. The real vessel grounded in a storm with a low battery after losing comms, and the model's risk rose to about 0.85 for the storm period.
- **Validation:** a sensitivity analysis on one input (sun exposure) and a by-eye match to what happened on that one mission.
- **Intended use:** mission planning and operator decision support. The model "can also give indications for when the human operator on shore should pay more attention".
-- same as us kinda

- We can get inspiration of their framework of calculating risk by external factors by using a bayesian network or a DBN.  Though different factors, similar idea. we also want to output a probability of necessity of human interaction.

> Optional idea: a BN fits your plan more than it might look. Their high/medium/low states look a lot like your V1 grid's bands, and learning a node's probability table from logged interventions is basically your V2 "per-cell frequencies" step. That gives you a positioning sentence: the same structure idea, but with probabilities learned from data instead of set by experts.

Pros:
- in depth risk calculation
- **Handles time:** risk is updated each step (day/night cycle, the storm), which a static risk analysis can't do.
- **Probability output:** an alert threshold could be set on it.
- **Built around a human supervisor** with a 2 h check-in, close to OOR's command every 2–3 h.

Cons:
- designed for a mission path

differences:
- uses wave-foil porpulsion

- **Probabilities are not learned:** they come from experts and assumptions. Table 4 marks current strength, initial battery and energy consumption as "Assumption".
- **Hard to use as an alert as-is:** P(failure) sits around 0.6–0.7 for almost the whole mission (Fig. 3). Any threshold low enough to catch the storm would fire nearly all the time.
- **No wind direction:** only wind speed is an input. For you, direction relative to the station is one of the main signals.

> **[Claude] Differences to our situation** (could become a row in your comparison table):
>
> | | Kristensen et al. 2022 | Our project |
> |---|---|---|
> | Vessel | AutoNaut: 5 m, wave-foil propulsion, solar for electronics, max 2 kn | OOR DataXplorer |
> | Mission | 19 days in a defined area off Norway, collecting data | Ongoing station keeping within 10 nm of Station 46012 |
> | What goes wrong | Power runs low, so SA, data collection and navigation degrade | Wind pushes the vessel toward the 10 nm limit |
> | Output | P(mission failure without manual intervention) at each 2 h step | P(pilot must intervene within Δt), e.g. Δt = 1 h |
> | Inputs | Sun, temperature, waves, wind speed, current, obstacles, comms coverage, battery | Position, distance to station, wind speed and direction |
> | Probabilities from | Experts, weather statistics, assumptions | V1: pilot rules; V2: learned from simulation and logged interventions |
> | Run on | Evidence set by hand from forecast and mission plan | Live telemetry |
> | Validation | One mission, sensitivity analysis | Recall, false alerts per shift, watch hours removed, against the V1 grid |
> | Human role | Shore operator checks every 2 h; model supports planning | Pilot moves from 24/7 watch to on-call alerts |
>
> **Where it goes in the background doc:** in 2.3, as the representative expert-based dynamic risk model (the physics/expert column of your hierarchy), and in Positioning as the work you *build on*. Use the same idea (a probability that a human must step in, to support an operator), but learned from telemetry, based on position, and checked against real pilot interventions.
