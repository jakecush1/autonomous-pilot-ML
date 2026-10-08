# Predicting Pilot Intervention for Station-Keeping USVs: A Brief Review

> **Graded items:** hierarchy drafted as Table 1 in §2. Still missing: comparison table and Venn diagram (Rowan, §3).

> **Length:** Jake's drafted sections come to about 1,000 words (intro 215, history 230, related work 560). Two ACM pages hold roughly 1,000–1,200 words of body text once the abstract, three tables/figures and the references are in, and Rowan's sections still need room, so plan to cut about a third. The note under each draft lists what to cut first.


## Abstract -jake

This paper gives a brief overview of the history and current state of human-monitored and autonomous station keeping for Uncrewed Surface Vehicles (USVs), focusing on whether the decision of *when human intervention is needed* can be automated. The Open Ocean Robotics (OOR) DataXplorer™ holds its position within 10 nm of a retired NOAA buoy station, with a pilot on 24/7 watch. The review covers a brief history of USVs and the relevant methods: control methods such as geofencing, drift prediction, dynamic risk assessment, and autonomous control versus operator supervision. Control methods hold position but do not predict when a human is needed. Drift and risk prediction methods give early warnings, but do not use past data to learn the probability that human intervention is needed. We propose a probability-based solution that uses live telemetry to predict when a pilot is needed. Code and related documents are available at https://github.com/jakecush1/autonomous-pilot-ML.


keywords: uncrewed surface vehicles, station keeping, human-in-the-loop, dynamic risk assessment, drift prediction.

>*Positioning* - by using methods in used in control methods, drift prediction, and risk assesment, we could build a probability based solution, considering all of these factors, to determine when human interaction is needed, effectively combining all methods to create a hybrid usv monitoring system.  Using live telemetry to predict when a pilot is needed. 


## 1. Introduction - Both read and research

*Station keeping* is the task of holding a vessel inside a bounded region despite wind, waves and current. On large ships it is solved by *dynamic positioning*: a closed-loop controller adjusts thrust continuously to hold position (1). The same control approach has been applied to small USVs (2). The DataXplorer has looser constraints: only has to stay within 10 nm of a retired buoy's position while a shore-based pilot on 24/7 watch issues a course correction when needed, usually when wind pushes it toward the edge. Here, Station keeping has two layers: a *control* layer that decides *how* the vessel holds position, and a *supervision* layer that decides *when* a human must step in. 

This research addresses the supervision layer: predicting from live telemetry whether a pilot will need to intervene within a future time window. Related work comes from three directions: station-keeping control (§2.1); drift prediction, which estimates where and when wind and current will carry a vessel to some boundary (§2.2); and dynamic risk assessment, which estimate when a mission is at risk and when to alert the human (§2.3). We first trace how the problem arose (§1.1), then compare these approaches and position our project among them (§3).

### 1.1 History - jake

U.S Coast Guard have been station keeping with crewed vessels collecting meterological data since 1940. (5) In 1970s this program was replaced by moored buoys, holding station passively on an anchor with no crew (6), reporting via satellites. Offshore drilling, meanwhile, automated *active* station keeping in the 1960s with dynamic positioning (1).

*Active station keeping means using power to hold station, passive station keeping is connected via static physical connection like anchor*

USV's have been in development for over 100 years, but the ability for them to be driven autonomously is a relatively new concept.  

Tesla demonstrated a radio-controlled boat in 1898, the Imperial German Navy used wire-guided explosive boats in the First World War, and by 1945 the U.S. Navy used remote-controlled boats for minesweeping and as targets, all within a short range of their operator (becuase they were radio)(7). In 1993 the first autonomous surface Craft (ASC) was created called ARTEMIS at MIT. only in the past few years have USV's been developed to a level to have impact in mission areas. (4) All these uncrewed boats were radio controlled, until MIT Sea Grant's ARTEMIS (1993) was among the first autonomous surface craft , this was a game changer(3), and then long-endurance USVs showed progression with the Wave glider and sail drone.  now USV's can now stand in for retired buoys, as the DataXplorer does for Station 46012. Military use has advanced in parallel: a century after the FL-boats, U.S. forces used three Saronic Corsair one-way attack USVs to strike a docked submarine at Iran's Bandar Abbas naval base in July 2026, the first U.S. combat use of sea drones (8).

"integrating machine learning to emulate human decision making, used to pilot marine vessels is a new concept."

4- [USV Development last 15 year](https://scispace.com/pdf/unmanned-surface-vehicles-15-years-of-development-4nxzuv0wq9.pdf)
5- [Alpha, Bravo, Charlie…](https://www.whoi.edu/?p=21599)
6- [The National Data Buoy Center: A History](https://www.ndbc.noaa.gov/ndbc-history.shtml)
7- [Unmanned Systems of World Wars I and II](https://www.penguin.com.au/books/unmanned-systems-of-world-wars-i-and-ii-9780262029223)
8- [CENTCOM Deploys Saronic Corsair USV Against Iranian Submarine at Bandar Abbas](https://www.navalnews.com/naval-news/2026/07/centcom-saronic-corsair-usv-strike-iran-submarine-bandar-abbas/)

## 2. Related Work

In the following sections we explore some of the most common methods and research done in field.  other reaserch (TTG's paper) explore time to run aground which can be looked as time until vessel crosses the 10nm boundary and the solution is virtually the same.  The paper also argues that distance alone (geofencing) is a weaker warning signal that a time-to-event estimation, accounting for drift.  this is an inspiration or userful reasearch information for our problem

Work related to supervised station keeping answers one of three questions (Table 1): 
- *how* to hold a vessel on station (station-keeping control, §2.1)
- *where and how soon* wind and current will carry it (drift prediction, §2.2)
- and *when* a mission is at risk and a human should act (risk assessment and operator supervision, §2.3). 

Within each, methods are either *model-based*, built from physics or expert judgement, or *data-driven*, learned from logged observations. Marine work is mostly model-based.


> | Question (level 1) | Model-based: physics or expert judgement | Data-driven or hybrid |
> |---|---|---|
> | **How to hold station** (§2.1) | *Trigger rule:* watch circle (9). *Feedback control:* dynamic positioning (1); PD, backstepping and sliding-mode control (2); heading into the disturbance (10) | ML-based control (11) |
> | **Where and how soon it will drift** (§2.2) | Time to grounding (12) | Physics model + neural correction (13) |
> | **When a human should act** (§2.3) | Qualitative hazard ID (14); fault tree + fuzzy BN (15); dynamic BN (16) | Takeover prediction, cars only (17); **marine: none found (this project)** |
>
> 9- [Wave Glider Product Sheet](https://web.archive.org/web/20230822211102/https://www.boeing.com/resources/boeingdotcom/defense/autonomous-systems/wave-glider-sharc/wave_glider_product_sheet.pdf)
> 10- [Nonlinear Station Keeping Control for Underactuated Unmanned Surface Vehicles to Resist Environmental Disturbances](https://doi.org/10.1016/j.oceaneng.2022.110603)
> 11- [Nonlinear and Machine-Learning-Based Station-Keeping Control of an Unmanned Surface Vehicle](https://doi.org/10.1115/OMAE2020-19276)
> 12- [Development of a Risk Indicator for Ship Drifting Groundings](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf)
> 13- [The Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipment Based on Fully Connected Neural Network (FCNN) Embedding Model](https://doi.org/10.3390/jmse12122262)
> 14- [Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships: Cognitive Model-Based Functional Analysis and Hazard Identification](https://doi.org/10.3390/jmse13050970)
> 15- [Risk Assessment of Maritime Autonomous Surface Ships Collisions Using an FTA-FBN Model](https://doi.org/10.1016/j.oceaneng.2024.118444)
> 16- [Dynamic Risk Analysis of Maritime Autonomous Surface Ships](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf)
> 17- [DeepTake: Prediction of Driver Takeover Behavior using Multimodal Data](https://doi.org/10.1145/3411764.3445563)
>
> LaTeX version (single column; needs `\usepackage{booktabs}`, which acmart already loads):
> ```latex
> \begin{table}[t]
>   \caption{Related work by the question each method answers (rows) and how its model is built (columns).}
>   \label{tab:hierarchy}
>   \small
>   \begin{tabular}{@{}p{0.22\columnwidth}p{0.42\columnwidth}p{0.28\columnwidth}@{}}
>     \toprule
>     & Model-based (physics / expert) & Data-driven / hybrid \\
>     \midrule
>     How to hold station (\S\ref{sec:control})
>       & Watch circle~\cite{liquidrobotics_waveglider}; DP~\cite{sorensen2011survey}; feedback control~\cite{sarda2016station,qu2022nonlinear}
>       & ML control~\cite{sinisterra2020ml} \\
>     Where it will drift (\S\ref{sec:drift})
>       & Time to grounding~\cite{dugan2024drifting}
>       & Neural correction~\cite{song2024drift} \\
>     When a human should act (\S\ref{sec:risk})
>       & Hazard ID~\cite{na2025qualitative}; FTA--FBN~\cite{li2024collision}; DBN~\cite{kristensen2022dynamic}
>       & Cars~\cite{pakdamanian2021deeptake}; \textbf{marine: this work} \\
>     \bottomrule
>   \end{tabular}
> \end{table}
> ```
>

> - **Level 1** is your own 2.1/2.2/2.3 split ("what question the method answers"). **Level 2** (model-based vs. data-driven) is the axis your project moves along, so the empty marine cell makes the positioning argument by itself.
> - **Not in the table:** Bogg & Birrell ([Do Not Adjust Your Set! How a Visual Alert Reduced Unnecessary Human Intervention in an Automated Vehicle](https://doi.org/10.54941/ahfe1007124)) is a user study of how an alert is *shown*, not a way of computing risk, so it doesn't fit either column. It stays in the §2.3 text. Chen et al. ([A Review of Risk Analysis Research for the Operations of Autonomous Underwater Vehicles](https://doi.org/10.1016/j.ress.2021.108011)) is a review; cite it in §2.3 rather than placing it in a cell.
> - **Sinisterra 2020** (from your proposal bib) is the only data-driven control entry, and I know it by title only. Skim it before citing, or leave that cell as "—".
> - **Table vs. figure:** the marking scheme says "Hierarchy + Figure". This table carries the same two levels as the manual's tree (Fig. 1) and is more compact. If you'd rather draw a tree, use the same rows and columns.
> - **Cut first if short on space:** the opening's last sentence.


### 2.1 station keeping control

#### Geofencing

> **[Claude] Draft 2.1 Station-keeping control** (about 170 words)

The simplest practice is a trigger rule: the vessel may drift freely inside some radius and is corrected only when it nears the edge- this is known as geofencing. OOR's pilots apply a similar practice at a large scale, correcting the DataXplorers navigation as it nears its 10 nm boundary. 

Feedback control instead corrects continuously. Dynamic positioning adjusts thrust to hold large ships within metres of a set point (1). Sarda et al. (2) applied the same idea to a 4 m USV, testing three controllers (proportional–derivative, backstepping and sliding mode), with and without wind measurements as an extra input. All three kept the average position error under about 3 m in 12-minute trials on sheltered water.  USVs that cannot thrust sideways instead point their bow into the combined push of wind, waves and current (10). 

Feedback controllers hold position with no human involved, but none predicts whether a correction will be needed later. Geofences are cheap and easy to understand, but they react to distance alone and ignore where the vessel is heading.



Other papers look at feedback closed-loop controllers that hold position (Sarda), while this would be beneficial to employing a autopilot control system which determines commands given the telemetry, this is out of scope for this project.  Though interesting, these papers do not allow for drift and are not framed around energy efficiency, but rather opimize heading and position accuracy.

Though these methods are useful in autonomous piloting, and certain aspects will be useful to consider in our design (such as live telemtry calculating to determine action, considering wind and location as input, general geofencing concepts), our solution aims to reduce human piloting time but not remove it.  

Geofencing limitations ignore when usv is drifting and only act when the usv reaches a limit.  Our solution aims to improve on this by constantly assessing distance.

#### Feedback loops

#### Weather optimal positioning
Another interesting approach to saving energy while geofencing is using Weather Optimal positioning -- which essentially is keeping the USV pointed into the wind to to minimize aerodynamic drag (10), (2).

> **[Claude] Link check:**
> - **(10)** (your "Paper" link) is **Qu & Cai, "Nonlinear station keeping control for underactuated unmanned surface vehicles to resist environmental disturbances", Ocean Engineering 246 (2022)**, doi:10.1016/j.oceaneng.2022.110603. It's paywalled, so I only read the abstract. An update law slowly turns the heading until it faces *against the combined disturbance* (unknown magnitude and direction). That's "into the disturbance", not specifically "into the wind to minimise aerodynamic drag", and the abstract doesn't mention energy.
> - **(2)** (your "(another)" link, arXiv 1702.04941) is **Sarda et al. 2016**, the same paper the intro cites as (2). It isn't a weather-optimal positioning paper. It compares PD, backstepping and sliding-mode controllers, with and without wind feedforward, on a 4 m, 180 kg WAM-V in 4–5 kn wind. Sliding mode did best, and feedforward only helped PD and backstepping in cross-wind. For a real weather-optimal positioning source, see its ref [53]: Kjerstad et al., "Weather Optimal Positioning Control for Marine Surface Vessels", IFAC CAMS 2010.



### 2.2 Drift prediction

Drifting trajectory is a difficult thing to do, but can be very beneficial in preventing accidents in the case of loss of propulsion.

Dugan presents the method used to calculate TTG - time to ground.  Though this paper surveys techniques to determine a drifting vessels TTG, the principles are the exact same for determining the time it would take for a vessel to drift k distance.  However all of these methods equate the drift time to be relative to wind. Note its simplified in their models

"FriisHansen [19] and Kystverket [20] use a uniform drift speed distribution between 1 and 3 m/s. Fowler and Sørgård [18] models the drift speed as 0.3 m/s in calm wind conditions and 0.9 m/s in stormy conditions. All equate the drift direction with the direction of the wind."

ocean currents are also considered "Sørgård and Vada [25] developed a drift trajectory prediction tool using two primary components: 1) estimating ocean current velocities, and 2) predicting the forced drift on a ship caused by wind and wave forces." when predicting drift.

accurately predicting these things require past data sets of "historical ocean forecast models to obtain wind speed, wind direction, wave height, wave period, wave direction, and sea-water velocity and direction"

We may want to follow a similar method if we are predicting drift.  this may be out of scope, however would be very useful.  Old data sets of the usv in the location could be used for this.

Conclusion - this paper predicts TTG which is the same process as drift prediction to outside of a operational zone which would be useful in a probability or more in depth prediction system.

largest take away : "All equate the drift direction with the direction of the wind."

[Development of Risk indicator for ship drifting ](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf)

> - **Output:** *time to grounding* (TTG), the expected time until a ship that loses propulsion would drift aground. It's recomputed along the voyage as an early warning.

Assessing other work (13) shows how using ML can greatly improve the accuracy of things like drift prediction, and consequently in our case would improve accuracy of probability in v2.  here is improved "the mean distance between predicted and actual track fell from **5.75 km to 0.41 km*" ~10x improvement in accuracy, using physics, simulations and ML.  Shows the benefit of data driven prediction models.

> - **Limitations (their §5.2):** the drift model was only validated on 250–270 m tankers, and it assumes constant weather, so it's less reliable beyond a few hours.

> Drift prediction estimates where wind and current will carry a vessel that is not being steered, such as a ship that has lost propulsion. Dugan and Utne (12) use it to compute time to grounding (TTG), the expected time until such a ship drifts aground, and update it along the voyage as an early warning. They note that earlier models assumed a fixed drift speed (e.g. 1–3 m/s) in the direction of the wind. Their model adds ocean current and wave forces from historical forecast data, and treats drift direction as uncertain. If the hazard is the DataXplorer's 10 nm boundary instead of shallow water, TTG becomes the time until the vessel leaves its station. TTG is purely physics-based, though, and was tested on one research-ship voyage with no real groundings. Song et al. (13) show the value of learning from data: a small neural network corrects a physics drift model each time the vessel reports its position, cutting mean track error from 5.75 km to 0.41 km. Both methods predict a path or a time; neither predicts whether a human will need to act.


>

### 2.3 Dynamic Risk assessment & supervision
#### DRA
Consider other risks, DRA, opertator alerting systems, forecast consideration?
- Dynamic Risk Assessment (DRA): [Risk assesment](https://www.sciencedirect.com/science/article/pii/S0029801824017827)
- [Dynamic Risk Assessment](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf)

> **[Claude] Link check:**
> - **The "Risk assesment" link** is **not** a dynamic risk paper. It's **Li, Wang & Yang, "Risk assessment of maritime autonomous surface ships collisions using an FTA-FBN model", Ocean Engineering 309 (2024)**. It covers *collision* risk: a fault tree mapped into a fuzzy Bayesian network, with probabilities from expert surveys because MASS failure data is scarce. It's static and design-level, not real-time. It could serve as the "static, expert-elicited" example in 2.3, or you could drop it, since collision isn't your failure mode. Open-access copy: [LJMU repository](https://researchonline.ljmu.ac.uk/id/eprint/24721/).
> - **The "Dynamic Risk Assessment" (PSAM16) link is your most important paper.** I read it in full: **Kristensen, Liu & Utne, "Dynamic Risk Analysis of Maritime Autonomous Surface Ships", PSAM16 2022.**
>   - A dynamic Bayesian network (DBN) estimates mission-failure risk from power management and situation awareness on a 5 m AutoNaut USV (wave-propelled, solar-powered).
>   - Case study: a 19-day mission off Norway, operating within a defined area. A shore operator checked in **every 2 hours**, which is also the DBN's time step. That's very close to OOR's pilot cadence. The real vessel grounded in a storm after losing communications with a low battery, and the model's risk rose before the event.
>   - Its probability tables come from system data plus expert judgement, and it was validated only by sensitivity analysis on that one mission.
>   - The authors say the model "can also give indications for when the human operator on shore should pay more attention". That's essentially your problem, so the claim in "Identified Gap in the Literature" needs softening. The idea already exists. What's missing is learning it from telemetry, applying it to position/boundary risk, and validating it against real intervention outcomes.

#### Operator supervision

bogg2026alert

> **[Claude]** Both `bogg2026alert` and DeepTake (Pakdamanian et al., CHI 2021, [arXiv:2012.15441](https://arxiv.org/abs/2012.15441)) are now in the 2.3 draft below. DeepTake predicts whether, how quickly and how well a driver takes over (96% accuracy on intention). That's the driver's *response*, not *whether* intervention is needed, so it's a contrast, not a competitor.

Other resources:
[The Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipmen](https://www.mdpi.com/2077-1312/12/12/2262)

[Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships](https://www.mdpi.com/2077-1312/13/5/970)

[Review of Risk analysis](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf)

> **[Claude]** What each "other resource" is:
> - **"Prediction and Dynamic Correction of Drifting Trajectory":** move to 2.2 (see the note there).
> - **"Qualitative Risk Assessment Methodology…":** **Na et al., "Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships: Cognitive Model-Based Functional Analysis and Hazard Identification" (COFA-HAZID), JMSE 13(5):970, 2025** (Korean Register). Design-phase and qualitative, with no numeric risk. It gives you a citable argument for dynamic over static assessment: systems that "drastically reduce human intervention" may require "real-time risk assessment methodologies". It also reports that STPA is the most-used qualitative method for MASS.
> - **"Review of Risk analysis":** **Chen, Bose, Brito, Khan, Thanyamanta & Zou, "A Review of Risk Analysis Research for the Operations of Autonomous Underwater Vehicles", Reliability Engineering & System Safety 216 (2021)** (abstract only; the PDF link blocked me). It reviews 42 papers, sorts methods into qualitative / semi-quantitative / quantitative, and recommends dynamic risk analysis and work on limited historical data. Its taxonomy could be your level-2 split for 2.3, and citing it backs up your hierarchy.
> - **Possibly useful for between 2.1 and 2.2:** Clark et al., "Station-Keeping Underwater Gliders Using a Predictive Ocean Circulation Model and Applications to SWOT Calibration and Validation", IEEE JOE, 2020 ([PDF](https://ai.jpl.nasa.gov/public/papers/clark-joe2019-station.pdf)). It does *predictive* station keeping from an ocean-current forecast, with simulation and field results. I only saw the abstract. (Not in the drafts or the bib.)

> **[Claude] Draft 2.3 Risk assessment and operator supervision** (about 190 words)
>
> Risk methods for autonomous marine vehicles range from qualitative to quantitative (18). Qualitative hazard identification lists what could go wrong before a trial and produces no numbers (14). Its authors note that systems which drastically reduce human intervention may need real-time risk assessment. Quantitative models such as a fault tree mapped into a fuzzy Bayesian network estimate collision probability, using expert surveys because failure data for autonomous ships is scarce (15). Kristensen et al. (16) make the estimate *dynamic*: a Bayesian network updated every two hours gives the probability of mission failure for a 5 m USV, which the authors suggest could tell a shore operator when to pay more attention. Its probabilities, however, come from experts and assumptions, and it was checked against a single mission. On the human side, Bogg and Birrell (19) found that remote operators of automated cars made fewer unnecessary interventions when shown a status alert, and DeepTake (17) learns from vehicle and driver data to predict whether and how quickly a driver will take over. We found no marine work that learns when a human must intervene from logged telemetry.
>
> 18- [A Review of Risk Analysis Research for the Operations of Autonomous Underwater Vehicles](https://doi.org/10.1016/j.ress.2021.108011)
> 19- [Do Not Adjust Your Set! How a Visual Alert Reduced Unnecessary Human Intervention in an Automated Vehicle](https://doi.org/10.54941/ahfe1007124)
>
> **[Claude] Notes on 2.3:**
> - **Order** runs static → dynamic → learned, which is the "how the field evolved" story manual §1.4 asks for, and it ends on the empty cell in Table 1.
> - **Kristensen is the closest prior work.** The draft gives it the most space and states its limits plainly (expert-set probabilities, one mission). That's what lets Rowan's gap claim be narrow and still true.
> - **Li 2024 (collision)** stays as the expert-elicited quantitative example. Grey it out in the Venn diagram as out of scope.
> - **The last sentence** is the gap, hedged with "we found". Rowan's §3 should repeat it in the narrowed form: learned from telemetry, about position/boundary risk, validated against real pilot interventions.
> - **Cut first if short on space:** the Na sentence about real-time assessment, then Li.


## 3.  Positioning Project - Rowan

1. propose a data driven model that mines historical telemetry (GPS, wind, current vectors) to predict boundary exceedance $t$ seconds into the future.
2.Real time risk scoring shifts operations from reactive thrusting to early, power-efficient drift mitigation.
3. **Human Integration:** Clear thresholds define when the system operates autonomously vs when human pilot.

> **[Claude]**
> - **Item 1:** "current vectors" aren't in the proposal; its state is position, wind speed and wind direction only. Either add currents to the scope (and say where the data would come from) or drop them. Also "$t$ *seconds*": the proposal's horizon Δt is on the order of an hour, so keep the units consistent.
> - **Item 2:** "reactive thrusting → power-efficient drift mitigation" isn't the proposal's motivation. The proposal is about pilot cost (moving from a 24/7 watch to on-call alerts), and its model only predicts *whether* intervention is needed, not what command to issue. Reframe item 2 around that.
> - **Item 3** fits the proposal's advisory alert, as long as it reads as "alert the on-call pilot" and not as switching the vessel between autonomy modes.
> - Manual §1.5: you don't need to claim novelty. Saying which approaches you build on, adapt, or compare against is enough. TTG (Dugan & Utne) and Kristensen's DBN are natural "build on / inspired by" choices. A simple distance-from-station threshold (the geofence rule) is the obvious **baseline** to compare your model against.

### Comparative analysis - Rowan

 - compare and contract each method
 - option a does x well, but lacks in y; option b does k well but lacks in z; our option does x y and z well. 

 some approaches to solving this problem are x, y z, and their shortcomings are a,b,c.
  - method 1 does a well but not b, method 2 does b well but not c; our method will take pros from 1 and 2 and do a, b and c

*NEED VEN DIAGRAMS AND TABLE IN THIS SECTION* see example for reference - venn diagram could be:
- A: station keeping
- B: drift prediction
- C: Dynamic Risk assessment
  - put relevent research in each circle, we are in the union of all of them

> **[Claude]**
> - Keeping this as its own section is fine, but it needs to come *before* Positioning (as 2.4 or section 3), not inside it. The marking scheme grades them separately (30% vs. 10%) and the manual orders them §1.4 then §1.5.
> - Jake's 2.1–2.3 drafts already explain each representative method briefly. This section should compare *across* them (the table and Venn) rather than re-describe each paper.
> - "Union" should be **intersection** (being in the union only means you're in at least one circle). With station keeping as one circle, the centre (station keeping ∩ drift prediction ∩ risk/supervision) is a defensible place for your project. Consider renaming circle C to "risk & operator supervision" so Kristensen 2022 and `bogg2026alert` both fit. Grey out what's out of scope, such as collision risk (Li 2024), like Fig. 2 in the manual.
> - Possible **table** columns, one row per representative paper: vehicle (ship / USV / AUV), inputs (position, wind, current, expert judgement), physics vs. data-driven, output (control command / trajectory / time-to-event / risk probability), real-time?, human in the loop?, evaluated on (simulation / one voyage / sea trials). The example uses ✓/✗ cells, which stay compact in two columns.


##### Existing Approaches and Their Limitations
Existing  solutions  fall into reactive control or model based trajectory estimators. While reactive geofences are computationally light, they are inherently backward-looking—initiating counter-thrust only after a vessel has drifted outside its designated boundary. This leads to excessive power consumption and increased risk of grounding in strong, dynamic currents. Conversely, physics-based predictive drift models and Dynamic Risk Assessment (DRA) frameworks offer proactive safety boundaries but heavily rely on explicit dynamic oceanographic models that are difficult to calibrate in real time.

> **[Claude]** The shape is good: it compares approaches instead of listing papers, which is what manual §1.4 asks for. But each claim needs a citation, and two don't match the papers:
> - "Counter-thrust only after… outside its boundary → excessive power consumption and grounding risk" has no source, and the control papers you linked aren't threshold-based.
> - "DRA frameworks … rely on explicit dynamic oceanographic models" fits TTG (NorKyst forecasts) and Song et al. (forecast wind/current), but not Kristensen's DBN. That model's weakness is expert-set probabilities validated on a single mission.

##### Identified Gap in the Literature
Most current frameworks treat station-keeping as a deterministic control problem or rely on static risk thresholds. There is a clear gap in utilizing [insert your ML focus here, e.g., historical trajectory data mining / probabilistic machine learning / Dynamic Risk Indicators] to predict drift probability dynamically under stochastic marine conditions before a boundary breach occurs. Furthermore, existing literature lacks a clear integration between dynamic risk scoring and automated human-intervention triggers.

> **[Claude]** The template placeholder `[insert your ML focus here, e.g., ...]` is still in the text. This paragraph can be the last paragraph of the comparative analysis, leading into Positioning. "Lacks a clear integration between dynamic risk scoring and … human-intervention triggers" is too strong given Kristensen et al. 2022 (§2.3), who propose exactly that link. Narrow the claim to what's actually missing: learned from telemetry, for boundary/position risk, and validated against real pilot interventions.
