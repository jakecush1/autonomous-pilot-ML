> | 7 | **Qu & Cai 2022**, "Nonlinear station keeping control for underactuated USVs…", Ocean Eng. 246. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0029801822000725) (paywalled; use the UVic library) | A second station-keeping control example (heading turns to face the disturbance) | Abstract + intro | 2.1 |

> [Claude] Paywalled, and I couldn't open it this time. This summary combines an earlier read of the abstract (noted in your background doc) with the abstract of the same authors' ICRA 2021 paper, which looks like the conference version of this work. Read the abstract and intro through the UVic library before citing details.

A control law for underactuated USVs (they can't push sideways) that holds position by turning the boat to face the combined wind, wave and current push.

- **Citation:** Yang Qu & Lilong Cai, "Nonlinear station keeping control for underactuated unmanned surface vehicles to resist environmental disturbances", Ocean Engineering 246 (2022) 110603. doi:10.1016/j.oceaneng.2022.110603.
- **Problem:** an *underactuated* USV has no sideways thrust, so it can't hold position if the disturbance hits it side-on. It has to turn to face the disturbance, but the direction and size of the disturbance are unknown.
- **Method (abstract):** an update law gradually turns the heading until it points against the *combined* environmental disturbance, while holding position.
- **Companion ICRA 2021 paper** (same authors, "Positioning Control for Underactuated Unmanned Surface Vehicles to Resist Environmental Disturbances"):
  - The controller keeps a fixed distance to a "look-ahead point", points the bow at it, and moves that point based on the position error.
  - The vessel ends up heading "counter to the direction of resultant environmental force".
  - Tested in simulation and "offshore in the face of wind and waves".
- **Energy:** the abstract doesn't mention energy, so don't cite it for "pointing into the wind to save energy".

- Link to us: is the DataXplorer underactuated too? If so, this is the closer control paper of the two (*check with OOR*).

Pros:
- Copes with an unknown disturbance direction without needing a wind or current sensor.
- Offshore experiments, at least in the ICRA version.

Cons:
- A control law only: no prediction and no human.
- Holds position at metre scale, not within a 10 nm zone.

> **Where it goes in the background doc:** 2.1, as a second control example (underactuated, weathervaning-style). One sentence is enough. Describe it as "turns into the combined disturbance", not "points into the wind".
