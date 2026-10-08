# Qu & Cai 2022: Station keeping for underactuated USVs by turning into the disturbance

- **Paper:** Yang Qu & Lilong Cai, "Nonlinear station keeping control for underactuated unmanned surface vehicles to resist environmental disturbances", Ocean Engineering 246 (2022) 110603. doi:10.1016/j.oceaneng.2022.110603.
- **Link:** [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0029801822000725) (paywalled; use the UVic library login)
- **Read:** abstract + intro. **Priority:** skim.
- **This summary:** written by Claude from the **abstract only** (an earlier read, noted in the background doc), plus the abstract of the same authors' ICRA 2021 paper, which looks like the conference version. Check details before citing.
- **Used in:** 2.1 Weather optimal positioning

**In one line:** a control law for underactuated USVs, which can't push sideways, that holds position by turning the bow into the combined wind, wave and current push.

## Summary

- **Problem:** an *underactuated* USV has no sideways thrust, so it can't hold position if the disturbance hits it side-on. It has to turn to face the disturbance, whose direction and size are unknown.
- **Method (abstract):** an update law gradually turns the heading until it points against the *combined* environmental disturbance, while holding position.
- **Companion ICRA 2021 paper** (same authors, "Positioning Control for Underactuated Unmanned Surface Vehicles to Resist Environmental Disturbances"):
  - The controller keeps a fixed distance to a "look-ahead point", points the bow at it, and moves that point based on the position error.
  - The vessel ends up heading "counter to the direction of resultant environmental force".
  - Tested in simulation and "offshore in the face of wind and waves".
- **Energy:** the abstract doesn't mention energy.

## Strengths and weaknesses

**Strengths**
- Copes with an unknown disturbance direction without needing a wind or current sensor.
- Offshore experiments, at least in the ICRA version.

**Weaknesses**
- A control law only: no prediction and no human.
- Holds position at metre scale, not within a 10 nm zone.

## How it relates to our paper

**The link:** a second example of the "how to hold station" line of work, for underactuated boats. Is the DataXplorer underactuated too? If so, this is the closer of the two control papers (*check with OOR*).

| Section | How to use it |
|---|---|
| 2.1 Weather optimal positioning | One sentence: the boat turns into the *combined* disturbance. This is the paper currently linked there. |
| Hierarchy figure | Station-keeping control × physics-based, next to Sarda. |
| Comparative analysis: table (Rowan) | Optional. Sarda is enough for the control row. |
| Comparative analysis: Venn (Rowan) | Circle A (station keeping) only. |

## To fix in the background doc

- 2.1 describes it as "keeping the USV pointed into the wind to minimize aerodynamic drag". It actually turns into the *combined* wind, wave and current disturbance, and the abstract doesn't mention energy or drag, so don't cite it for energy savings.
