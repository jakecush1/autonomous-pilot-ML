> | 8 | **Na et al. 2025**, qualitative MASS risk (COFA-HAZID), JMSE 13:970. [MDPI](https://www.mdpi.com/2077-1312/13/5/970) | A one-line citation for "static/design-phase risk isn't enough; real-time assessment is needed" | Abstract + intro | 2.3 |

> [Claude] Written by Claude from the full paper (30 pp). These aren't your own notes, so check them against the paper before using them in the review.

A qualitative risk assessment method for autonomous ships, from the Korean Register (a ship classification society). It's for the design and trial phase and produces no numbers. Useful for one sentence: once humans are taken out of the loop, design-phase risk assessment isn't enough and real-time risk assessment is needed.

- **Citation:** Na, Lee, Baek, Kim & Choung, "Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships: Cognitive Model-Based Functional Analysis and Hazard Identification", JMSE 13(5):970, 2025. Korean Register, Busan.
- **Goal:** a structured way to find hazardous scenarios in MASS operations, so MASS can be compared with conventional ships and designs and trials can be approved.
- **Method (COFA-HAZID):**
  1. **Functional analysis:** break the ship's operation into functions. Each function is a "Functional Block" modelled on a cognitive / intelligent-agent loop (sense → decide → act), and the blocks connect into a Functional Flow Diagram.
  2. **HAZID:** a workshop-style hazard identification that asks how each function could degrade or fail, and what happens if it does.
  3. Logic gates (AND/OR) inside the blocks let the diagram be converted into a fault tree or reliability block diagram later, for quantitative analysis.
- **Bigger framework (their Fig. 1; not carried out in this paper):** design-phase assessment is followed by an operational phase. There, real-time data (system reliability, traffic density, weather) feeds a "Risk Model Generator", and a **real-time risk indicator** is shown to "human operators or autonomous systems".
- **Case study:** a qualitative risk assessment for a sea trial of K-ANS, an autonomous navigation system on an 1800 TEU container ship, under the IMO's interim guidelines for MASS trials.
- **Findings from trials (§4.1):**
  - The officer of the watch (OOW) stays in charge and takes control back when the system fails.
  - The key risk is the **handover between autonomous and manual control**.
  - The OOW has to monitor the system *and* carry out normal duties, which adds workload.
- **Literature note:** the reviews they cite find STPA is the most-used qualitative method for MASS, and Bayesian networks the most-used quantitative one.
- **Key quote (§2.1):** "to operate advanced systems that drastically reduce human intervention, one may be required to implement real-time risk assessment methodologies to evaluate various dynamic operational variables and support decision-making (whether by humans or the system)".
- **Future work:** a prototype real-time risk monitoring system for MASS (R2-MAS).

- Link to us: that quote is our motivation in one line. The OOW's monitoring burden is the same problem as our pilot on 24/7 watch.

Pros:
- A citable statement that static, design-phase risk assessment isn't enough for systems with less human involvement.
- Recent (2025) and from a classification society. Also confirms STPA and BNs as the common methods.
- Names the human-handover problem directly.

Cons:
- Qualitative only: no numbers and no probabilities.
- Done before operation (for approval), not in real time. The real-time part is only proposed.
- Focused on navigation and collision for a large container ship, not on station keeping.

> **[Claude] Differences to our situation** (could become a row in your comparison table):
>
> | | Na et al. 2025 | Our project |
> |---|---|---|
> | Vessel | 1800 TEU container ship with an autonomous navigation system (trial) | OOR DataXplorer |
> | When | Design / before the trial | Live, during operation |
> | Output | List of hazardous scenarios and risk controls (qualitative) | P(pilot must intervene within Δt) |
> | Method | Functional analysis + expert HAZID workshop | V1: pilot-rule grid; V2: learned from logged interventions |
> | Data | Expert judgement | Telemetry + logged interventions |
> | Human role | OOW supervises the system and takes over on failure | Pilot moves from 24/7 watch to on-call alerts |
>
> **Where it goes in the background doc:** 2.3, in one line, as the qualitative / static example and the motivation for real-time assessment. It's also the "qualitative" leaf under Chen's taxonomy.
