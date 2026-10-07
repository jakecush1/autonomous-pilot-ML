>  Reading list (most important first).** 

> | 3 | **Sarda et al. 2016**, "Station-keeping control of a USV exposed to current and wind disturbances", Ocean Eng. 127 (already `sarda2016station`). [arXiv](https://arxiv.org/pdf/1702.04941) | Your representative station-keeping control paper; its §II is a mini-survey of station-keeping control | Abstract, §I–II, conclusions (long paper; skip the maths) | 2.1, comparison |

> | 1 | **Kristensen, Liu & Utne 2022**, "Dynamic Risk Analysis of Maritime Autonomous Surface Ships", PSAM16. [PDF](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf) | Closest prior work: risk model for a USV with a shore operator checking in every 2 h; suggests the model can tell the operator when to pay attention | **All** (12 pp) | 2.3, comparison, positioning |


> | 4 | **Song et al. 2024**, "Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipment…", JMSE 12:2262. [MDPI](https://www.mdpi.com/2077-1312/12/12/2262) | The only data-driven drift paper you have (physics model + neural-network correction) | Abstract, method overview, results, §5 limitations | 2.2, comparison |


> | 2 | **Dugan & Utne 2024**, "Development of a risk indicator for ship drifting groundings", PSAM17. [PDF](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf) | Time-to-event early warning built from drift; argues that distance alone is a weak signal. Replace "ground" with "10 nm boundary" | **All** (10 pp) | 2.2, comparison, positioning |

> | 5 | **Manley 2008**, "Unmanned surface vehicles, 15 years of development", OCEANS 2008. [link](https://scispace.com/pdf/unmanned-surface-vehicles-15-years-of-development-4nxzuv0wq9.pdf) | The history source; replaces the Wikipedia links | History sections | 1.1 |

> | 6 | **Chen et al. 2021**, "A Review of Risk Analysis Research for the Operations of AUVs", RESS 216. [PDF](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf) | Its qualitative / semi-quantitative / quantitative taxonomy can justify your hierarchy for 2.3 | Abstract + taxonomy section only | 2 overview, 2.3 |

> | 7 | **Qu & Cai 2022**, "Nonlinear station keeping control for underactuated USVs…", Ocean Eng. 246. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0029801822000725) (paywalled; use the UVic library) | A second station-keeping control example (heading turns to face the disturbance) | Abstract + intro | 2.1 |

> | 8 | **Na et al. 2025**, qualitative MASS risk (COFA-HAZID), JMSE 13:970. [MDPI](https://www.mdpi.com/2077-1312/13/5/970) | A one-line citation for "static/design-phase risk isn't enough; real-time assessment is needed" | Abstract + intro | 2.3 |

> | 9 | `bogg2026alert` (already in the proposal bib) | Operator alerting in automated vehicles | Whatever you used for the proposal | 2.3 Operator supervision |
>
> **Optional or new finds:** DeepTake ([arXiv:2012.15441](https://arxiv.org/abs/2012.15441); data-driven takeover prediction in cars), the Wave Glider [product sheet](https://www.boeing.com/resources/boeingdotcom/defense/autonomous-systems/wave-glider-sharc/wave_glider_product_sheet.pdf) (a "watch circle" source for the geofence approach), and Clark et al., IEEE JOE 2020 ([PDF](https://ai.jpl.nasa.gov/public/papers/clark-joe2019-station.pdf); predictive station keeping). **Probably drop:** Li et al. 2024 (the collision FTA-FBN paper behind the "Risk assesment" link in 2.3), since collision isn't your failure mode.

