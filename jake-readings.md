# Jake: suggested readings

For my sections: **Abstract, 1. Introduction, 1.1 History**, and the **2.1 / 2.2** drafts. Background doc due **Oct 7 (AoE)**.

Ranked by how much each paper changes what I write. Total reading time is about 1 h 45 min.

## Read these (about 1.5 h)

| # | Paper | What to read | Time | Why | Section | Notes |
|---|---|---|---|---|---|---|
| 1 | **Manley 2008**, "Unmanned surface vehicles, 15 years of development", OCEANS 2008. [IEEE Xplore](https://ieeexplore.ieee.org/document/5152052) (paywalled, so use the UVic library login) | History sections | 20 min | The only history source for 1.1. It replaces the Wikipedia links and fixes the timeline (Fernlenkboote dates, the 1940s–90s block, the ARTEMIS year) | 1.1 | [checklist](summaries/USV%2015%20Years%20of%20Development.md) |
| 2 | **Dugan & Utne 2024**, "Development of a risk indicator for ship drifting groundings", PSAM17. [PDF](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf) | All (10 pp) | 40 min | Core of 2.2, and the argument that distance alone (geofencing) is a weak signal. My §2 intro already relies on it | 2.1, 2.2 | [summary](summaries/Drifting%20Grounding%20Risk%20Indicator.md) |
| 3 | **Sarda et al. 2016**, "Station-keeping control of an unmanned surface vehicle exposed to current and wind disturbances", Ocean Eng. 127. [arXiv](https://arxiv.org/pdf/1702.04941) | Abstract, §I–II, the §VII results tables, §VIII conclusions. Skip §III–VI (the maths) | 25 min | The 2.1 control paper; §II is a mini-survey to cite. It's **not** a weather-optimal positioning paper, so fix that line | 2.1 | [summary](summaries/station-keeping%20control%20of%20usv.md) |

## Skim these (about 5 min each)

| Paper | What to read | Why | Section | Notes |
|---|---|---|---|---|
| **Song et al. 2024**, drift trajectory + FCNN correction, JMSE 12:2262. [MDPI](https://www.mdpi.com/2077-1312/12/12/2262) | Abstract, Fig. 1, §5 | The only data-driven drift paper; fills the data-driven cell for 2.2 | 2.2 | [summary](summaries/Drift%20Trajectory%20Prediction%20FCNN.md) |
| **Qu & Cai 2022**, nonlinear station keeping for underactuated USVs, Ocean Eng. 246. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0029801822000725) (UVic login) | Abstract | One sentence in 2.1: the boat turns into the *combined* disturbance. Don't cite it for energy savings | 2.1 | [summary](summaries/Nonlinear%20Station%20Keeping%20Underactuated%20USV.md) |
| **Chen et al. 2021**, review of AUV risk analysis, RESS 216. [PDF](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf) | Abstract + taxonomy section | Only if I'm drawing the hierarchy figure: qualitative / semi-quantitative / quantitative split | 2 overview | [summary](summaries/Risk%20Analysis%20Review%20AUVs.md) |
| **Na et al. 2025**, COFA-HAZID, JMSE 13:970. [MDPI](https://www.mdpi.com/2077-1312/13/5/970) | Abstract + first part of §2.1 | One citation: "systems that drastically reduce human intervention … real-time risk assessment" | Intro, 2.3 | [summary](summaries/Qualitative%20Risk%20Assessment%20MASS.md) |

## Skip

- **Kristensen et al. 2022**: already read ([my notes](summaries/Dynamic%20Risk%20Analysis.md)).
- **Bogg & Birrell 2026** (`bogg2026alert`): read for the proposal ([summary](summaries/Visual%20Alert%20Remote%20Operator.md)).
- **Li et al. 2024** (collision FTA-FBN): drop it, since collision isn't our failure mode.
- **Optional, only if there's time:** DeepTake ([arXiv:2012.15441](https://arxiv.org/abs/2012.15441)), Clark et al. 2020 ([PDF](https://ai.jpl.nasa.gov/public/papers/clark-joe2019-station.pdf)). Open the Wave Glider [product sheet](https://www.boeing.com/resources/boeingdotcom/defense/autonomous-systems/wave-glider-sharc/wave_glider_product_sheet.pdf) only to pull the 30 m watch-circle number if I cite it.

## Notes

- **Abstract and Intro need no new reading.** Write them last, from what ends up in the other sections.
- **History after 2008:** Manley stops in 2008. If 1.1 mentions Saildrone (founded 2012) or ML, it needs a second, more recent source.
- **AI rule (Guideline C):** the summaries in `summaries/` marked `[Claude]` aren't my own notes. Write the review from my own reading of the papers.
