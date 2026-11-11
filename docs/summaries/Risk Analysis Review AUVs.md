# Chen et al. 2021: Review of risk analysis for autonomous underwater vehicles

- **Paper:** Chen, Bose, Brito, Khan, Thanyamanta & Zou, "A Review of Risk Analysis Research for the Operations of Autonomous Underwater Vehicles", Reliability Engineering & System Safety 216 (2021) 108011. doi:10.1016/j.ress.2021.108011.
- **Link:** [PDF (Southampton repository)](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf). This blocked automated access but should open in a browser.
- **Read:** abstract + the taxonomy section. **Priority:** skim, and only if you're drawing the hierarchy figure.
- **This summary:** written by Claude from the **abstract only**. Fill in the taxonomy section after reading.
- **Used in:** 2 Related Work intro / hierarchy figure · 2.3 DRA · Identified gap

**In one line:** a review of 42 risk analysis papers for AUVs. It's mainly useful for how it groups risk methods.

## Summary

- **Goal:** a systematic review of risk analysis for AUV operations, "to assist decision making for safer operations".
- **Method:** retrieve and analyse 42 papers, identify the critical risk factors and causal relationships, and compare methods grouped as **qualitative, semi-quantitative and quantitative**.
- **Findings (abstract):**
  - As AUVs mature, "environmental factors, human factors, and their interactive impacts are gathering more attention".
  - Quantitative methods have "recently played a key role in improving the accuracy and handling the uncertainties of risk estimation".
- **Recommended future work:** "dynamic risk analysis, addressing limited historical data, intelligent risk analysis, and multi-vehicles risk analysis".

**To fill in from the taxonomy section:** which methods sit under each category (e.g. FMEA/HAZID as qualitative? risk matrices as semi-quantitative? BN/FTA as quantitative?), and whether any are data-driven → *to fill in*

## Strengths and weaknesses

**Strengths**
- A published taxonomy you can cite for the hierarchy, so it isn't one you invented.
- An independent call for dynamic risk analysis and for work with limited data.

**Weaknesses**
- About AUVs, not surface vehicles.
- A review, not a method, so it has nothing to compare against directly.

## How it relates to our paper

**The link:** three of its four future-work directions describe our project: dynamic (updated live), limited historical data (few logged interventions), and intelligent (learned).

| Section | How to use it |
|---|---|
| 2 Related Work intro / hierarchy figure | Its qualitative / semi-quantitative / quantitative split can be the level-2 split for the risk branch: Na 2025 is qualitative, Kristensen 2022 is quantitative. |
| 2.3 DRA | Background citation showing that risk analysis for autonomous vehicles is an active, reviewed field. |
| Identified gap (Rowan) | Its future-work list supports the gap claim with someone else's words: dynamic risk analysis with limited historical data is still open. |
| Comparative analysis: table / Venn (Rowan) | Not needed, since it's a review rather than a method. |
