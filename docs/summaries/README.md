# Paper summaries: index

One file per paper, all in the same layout: header, one-line summary, Summary, Strengths and weaknesses, **How it relates to our paper** (a table by section), Compared with our project, To fix in the background doc.

Kristensen is the only file with Jake's own notes. The rest were written by Claude and should be checked against the papers before use.

## Papers

| Paper | File | Summary based on | Hierarchy cell | Venn |
|---|---|---|---|---|
| Kristensen, Liu & Utne 2022 | [Dynamic Risk Analysis](Dynamic%20Risk%20Analysis.md) | Full paper | Risk × expert-based | C |
| Dugan & Utne 2024 | [Drifting Grounding Risk Indicator](Drifting%20Grounding%20Risk%20Indicator.md) | Full paper | Drift × physics-based | B ∩ C |
| Sarda et al. 2016 | [station-keeping control of usv](station-keeping%20control%20of%20usv.md) | Full paper | Control × physics-based | A |
| Song et al. 2024 | [Drift Trajectory Prediction FCNN](Drift%20Trajectory%20Prediction%20FCNN.md) | Full paper | Drift × data-driven/hybrid | B |
| Na et al. 2025 | [Qualitative Risk Assessment MASS](Qualitative%20Risk%20Assessment%20MASS.md) | Full paper | Risk × expert-based (qualitative) | C |
| Bogg & Birrell 2026 | [Visual Alert Remote Operator](Visual%20Alert%20Remote%20Operator.md) | Full paper | Operator supervision | C* |
| Qu & Cai 2022 | [Nonlinear Station Keeping Underactuated USV](Nonlinear%20Station%20Keeping%20Underactuated%20USV.md) | Abstract only | Control × physics-based | A |
| Chen et al. 2021 | [Risk Analysis Review AUVs](Risk%20Analysis%20Review%20AUVs.md) | Abstract only | Gives the level-2 split for risk | none |
| Manley 2008 | [USV 15 Years of Development](USV%2015%20Years%20of%20Development.md) | Abstract only | none (history) | none |

Hierarchy: level 1 = what question the method answers (2.1 control / 2.2 drift / 2.3 risk & supervision); level 2 = physics/expert-based vs data-driven. **Risk × data-driven is empty, and that's where our project sits.**
Venn: A = station keeping, B = drift prediction, C = dynamic risk assessment. Our project is the intersection A ∩ B ∩ C. *Bogg only fits C if it's renamed "risk & operator supervision".

## Which summaries to open, by section

| Section | Owner | Summaries |
|---|---|---|
| Abstract / 1. Introduction | Jake / both | Kristensen (the reason to narrow "none of these methods…"), Na (real-time motivation quote), Sarda + Bogg (the two lines already cited in the proposal intro) |
| 1.1 History | Jake | Manley (main source), Dugan & Utne intro (drifting-ship accidents, VTS), Sarda §I (what USVs are used for) |
| 2 Related Work intro + hierarchy figure | | Chen (taxonomy), plus the cells in the table above |
| 2.1 Station keeping control | | Sarda (feedback loops), Qu & Cai (weather optimal positioning), Dugan & Utne (the case against distance-only geofencing) |
| 2.2 Drift prediction | | Dugan & Utne (physics, time-to-event), Song (hybrid, learned) |
| 2.3 DRA | | Kristensen (dynamic, expert-based), Na (qualitative, static), Chen (review) |
| 2.3 Operator supervision | | Bogg & Birrell (main), Na (handover risk) |
| Comparative analysis: table + Venn | Rowan | Rows: Sarda, Dugan & Utne, Song, Kristensen, Bogg (Na optional). Each file has a "Compared with our project" table to draw from. |
| Existing approaches & limitations | Rowan | Dugan & Utne + Song (depend on forecast data), Kristensen (expert-set, one mission), Na (static) |
| Identified gap | Rowan | Kristensen (narrow the claim), Chen (future-work list), Na (real-time is needed) |
| 3. Positioning | Rowan | Build on: Kristensen, Dugan & Utne. Method idea: Song. Baseline: the geofence/distance rule (Dugan & Utne). |
