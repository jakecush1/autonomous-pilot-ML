# Na et al. 2025: Qualitative risk assessment for autonomous ships (COFA-HAZID)

- **Paper:** Na, Lee, Baek, Kim & Choung, "Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships: Cognitive Model-Based Functional Analysis and Hazard Identification", J. Mar. Sci. Eng. 13(5):970, 2025. Korean Register, Busan.
- **Link:** [MDPI](https://www.mdpi.com/2077-1312/13/5/970) (open access)
- **Read:** abstract + the first part of §2.1 (where the key quote is). **Priority:** skim.
- **This summary:** written by Claude from the full paper (30 pp). Not Jake's own notes; check it against the paper before using it in the review.
- **Used in:** Intro · 2.3 DRA · 2.3 Operator supervision · Existing approaches & limitations

**In one line:** a structured, workshop-style method for listing what could go wrong with an autonomous ship, used before trials and producing no numbers. It's useful mainly for one quote: once humans are taken out of the loop, real-time risk assessment is needed.

## Summary

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
- **Literature note:** the reviews they cite find that STPA is the most-used qualitative method for MASS, and Bayesian networks the most-used quantitative one.
- **Key quote (§2.1):** "to operate advanced systems that drastically reduce human intervention, one may be required to implement real-time risk assessment methodologies to evaluate various dynamic operational variables and support decision-making (whether by humans or the system)".
- **Future work:** a prototype real-time risk monitoring system for MASS (R2-MAS).

## Strengths and weaknesses

**Strengths**
- A citable statement that static, design-phase risk assessment isn't enough for systems with less human involvement.
- Recent (2025) and from a classification society. It also confirms STPA and BNs as the common methods.
- Names the human-handover problem directly.

**Weaknesses**
- Qualitative only: no numbers and no probabilities.
- Done before operation (for approval), not in real time. The real-time part is only proposed.
- Focused on navigation and collision for a large container ship, not on station keeping.

## How it relates to our paper

**The link:** the §2.1 quote is our motivation in one line. The OOW's monitoring burden is the same problem as our pilot on 24/7 watch.

| Section | How to use it |
|---|---|
| Abstract / 1. Introduction | Motivation: systems that "drastically reduce human intervention" may need real-time risk assessment. |
| 2.3 DRA | The qualitative / static example, in contrast with Kristensen's dynamic model. The STPA/BN finding can back up a sentence on which methods are common. |
| 2.3 Operator supervision | Supporting point: in real trials the human must monitor the system and take over, and the handover is a key risk. |
| Hierarchy figure | Risk & supervision × expert-based (the qualitative leaf if you use Chen's split). |
| Comparative analysis: Venn (Rowan) | Circle C (risk). |
| Comparative analysis: table (Rowan) | Optional row; see the table below. |
| Existing approaches & limitations (Rowan) | Static, design-phase assessments can't follow conditions as they change. |

## Compared with our project

| | Na et al. 2025 | Our project |
|---|---|---|
| Vessel | 1800 TEU container ship with an autonomous navigation system (trial) | OOR DataXplorer |
| When | Design / before the trial | Live, during operation |
| Output | List of hazardous scenarios and risk controls (qualitative) | P(pilot must intervene within Δt) |
| Method | Functional analysis + expert HAZID workshop | V1: pilot-rule grid; V2: learned from logged interventions |
| Data | Expert judgement | Telemetry + logged interventions |
| Human role | OOW supervises the system and takes over on failure | Pilot moves from 24/7 watch to on-call alerts |

## To fix in the background doc

- It's listed under "Other resources" at the end of 2.3. Move it into the DRA subsection.
