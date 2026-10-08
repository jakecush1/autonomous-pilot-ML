# Predicting Pilot Intervention for Station-Keeping USVs: A Brief Review

> 2. **Station-keeping framing (updated):** your framing works: station-keeping literature belongs in the review, and its gaps motivate your system. Be precise about *which part* you improve, though. Your model doesn't issue commands (proposal: it "predicts only whether intervention is required"), so the improvement is to station-keeping *supervision* (when a human must act), not to the *control law* that holds position. The proposal's intro calls control-law work "a different problem", so add one sentence in this document that bridges the two (control = how the vessel holds station; this project = supervising station keeping) so a marker doesn't see a contradiction.

> 4. **Graded items still missing:** abstract, hierarchy figure, comparison table, Venn diagram.


## Abstract -jake

This paper is a brief overview of the history and current state of human monitored, and autonomous methods for station keeping using an Uncrewed Surface Vehicle (USV), and more specifically looking at the determining if we can automate the decision of *When human intervention is needed* while utilizing common semi-autonomous station keeping methods.  Open Ocean Robotics (OOR) DataXplorer(^tm) holds within 10nm of a retired NOAA buoy station, with a pilot on 24/7 watch.  By analyzing current methods, we hope to develop a more efficient method to reduce the labor necessary to complete this task.  The review covers a brief history of USV's and relevent methods: control methods like Geo-fencing, drift prediction, dynamic risk assesment, and autnomous control vs operator supervision.  

None of these methods explore the problem of hybrid station keeping, which asks the question of determining *When* human interaction is needed. Control methods hold position, but dont predict when a human is needed.  Drift or risk prediction algorithms give early warnings, which is a benficial method in predicting when a human would be needed.  If we can combine the outcomes from all of these we can start to think of a superior solution which would could save lots of money in labor.

by using methods in used in control methods, drift prediction, and risk assesment, we could build a probability based solution, considering all of these factors, to determine when human interaction is needed, effectively combining all methods to create a hybrid usv monitoring system.  Using live telemetry to predict when a pilot is needed.  You can find code and more documents relating to this subject at https://github.com/jakecush1/autonomous-pilot-ML


keywords: unmanned surface vehicles, station keeping, human-in-the-loop, dynamic risk assessment, drift prediction.

> **[Claude] Abstract vs. Introduction.** Below are your own sentences sorted into the two places, with the wording unchanged. `[…]` marks a suggested cut.
>
> **Abstract** (make it one paragraph; it's currently about 260 words, so aim for roughly 120):
> This paper is a brief overview of the history and current state of human monitored, and autonomous methods for station keeping using an Uncrewed Surface Vehicle (USV), and more specifically looking at the determining if we can automate the decision of *When human intervention is needed* […]. Open Ocean Robotics (OOR) DataXplorer(^tm) holds within 10nm of a retired NOAA buoy station, with a pilot on 24/7 watch. The review covers a brief history of USV's and relevent methods: control methods like Geo-fencing, drift prediction, dynamic risk assesment, and autnomous control vs operator supervision. Control methods hold position, but dont predict when a human is needed. Drift or risk prediction algorithms give early warnings […]. […] we could build a probability based solution […] to determine when human interaction is needed […]. Using live telemetry to predict when a pilot is needed. You can find code and more documents relating to this subject at https://github.com/jakecush1/autonomous-pilot-ML
>
> **Introduction** (motivation and the term you're introducing):
> By analyzing current methods, we hope to develop a more efficient method to reduce the labor necessary to complete this task. None of these methods explore the problem of hybrid station keeping, which asks the question of determining *When* human interaction is needed. […] If we can combine the outcomes from all of these we can start to think of a superior solution which would could save lots of money in labor.
>
> **§3 Positioning, not the abstract:** the full "by using methods in used in control methods, drift prediction, and risk assesment … hybrid usv monitoring system" sentence. The abstract keeps only its core (above).
>
> **Why these moves and what to fix:**
> - **What the abstract is for:** saying what the paper covers and what it concludes. Motivation (labour cost), defining a new term, and the detailed plan belong in the Introduction and Positioning.
> - **Sentence 1:** I cut "while utilizing common semi-autonomous station keeping methods" because the sentence is already long and the station-keeping context is in the next sentences. "Looking at the determining if we can automate" doesn't parse, so rephrase it.
> - **"None of these methods explore…"** is too strong given Kristensen 2022, whose risk model is meant to show when the operator should pay attention. Narrow it (for example, none *learn* this from telemetry). "Hybrid station keeping" is your own term, so define it in the Introduction before using it.
> - **The early-warning sentence** needs its second half for the abstract to state a gap: what limits drift and risk methods (physics- or expert-based, each validated on a single voyage or mission).
> - **"Superior solution" and "lots of money"** are informal and unsupported. Your proposal has the actual figure (about 1,095 eight-hour pilot shifts a year), so use that in the Introduction.
> - **Repo sentence:** keep it. Manual §1.6.2 requires the repo to be linked in the abstract.
> - **Keywords:** in LaTeX these go in `\keywords{}`, separate from the abstract text, as in the example template.
> - **Typos:** relevent, assesment, autnomous, benficial, dont, "would could", "methods in used in". For "DataXplorer(^tm)", use `DataXplorer\texttrademark{}` or drop the ™.

## 1. Introduction - Both read and research
Our problem is exploring the idea of "if we can determine *When* a human interaction is needed, while station keeping with a USV".  In exploring this topic we found it import to first explore the most popular methods of station keeping used in the industry.

- what approaches have been used to address OUR problem: while station keeping with a USV, when is human interaction needed?

Here is our specific problem at the company. we care because - having to pay someone is expensive


3 methods used in automated marine station keeping, and USV station keeping which are relevant to our problem.  These are current popular methods which are researched, simulated, tested and used.  Ideally our method or solution would combine all of these methods, considering all research and creating a probability rating which considers geofencing and usv location relative to its station, calcualtes a drift prediction based on current telemetry, and considers other data to influence the probabilty encompassing risk assessment.


### 1.1 History - jake

origin and evolution of the problem, context for those not familiar. where the problem came from, why its important to CS and ML trace problem back to its eariliest roots, even before CS. earliest ideas, practices or challenges that are related to the problem 
- do not give exhaustive history, give quick journey from early origins to modern

1993 first ASC created called ARTEMIS at MIT. only in the past few years have USV's been developed to a level to have impact in mission areas. [history](https://scispace.com/pdf/unmanned-surface-vehicles-15-years-of-development-4nxzuv0wq9.pdf)


"integrating machine learning to emulate human decision making to used to pilot marine vessels

1898: Nikola Tesla 1898 - teleautomaton boat radio controlled
1914: WW1 - german army developed fernlenkboote - radio controlled motorboats packed with explosives to ram british warships
1940s - 1990s: WW2 - US navy began converting conventional small vessels into remote controlled boats for mine sweeping to clear waters
    - all of these were limited to short range radio proximity
1990-2010: MIT sea grant developed ARTEMIS
    - [Liquid robotics](https://en.wikipedia.org/wiki/Liquid_Robotics#Wave_Glider): wave glider
    - [Saildrone](https://en.wikipedia.org/wiki/Saildrone_(company))
2020s - present: drone boats

[USV Development last 15 year](https://scispace.com/pdf/unmanned-surface-vehicles-15-years-of-development-4nxzuv0wq9.pdf)

USV's have been in development for over 100 years, but the ability for them to be driven autonomously is a relatively new concept.  This topic of autonomous driving, humanless piloting, is popular and new.  Autonomous Robotics is a huge topic in ML and CS.  Most people think humanoid, but the development of autonomous piloting and robotics development are all closely related.  Methods in autonmous driving cars have been largely explored and developed likely due to the demand in market, where USV autonmous piloting market lags behind this as its a more niche market.



> **[Claude]** History notes:
> - The manual asks for the earliest roots of the *problem*. The example starts from the problem itself (1927 voting blocs), not the technology. Your timeline is a history of unmanned boats, but the proposal's problem is *keeping a vessel on station and knowing when a human needs to step in*. 

> Your notes on weather reporting and captains' decisions are closer to that root. Consider leading with them, then the remote-control timeline, then where ML enters.

> - "1914: WW1 - german army…": the Fernlenkboote were built for the Imperial German *Navy*, not the army, and I believe they were used in combat around 1916–17. Check "1914".
> - "1940s - 1990s" covers 50 years. The "USV Development last 15 year" paper is the source to split it up.
> - "1990-2010": Saildrone was founded in 2012, which is outside that range.
> - "USV Development last 15 year" is **Manley, J., "Unmanned surface vehicles, 15 years of development", MTS/IEEE OCEANS 2008** (doi:10.1109/OCEANS.2008.5152052). It's ref [1] in Sarda et al. Cite it instead of the Wikipedia links; the manual asks for textbooks, surveys, influential papers or reliable technical sources. (scispace blocked me, so I haven't read the body.)
> - "Most people think humanoid…" is off-topic for a 2-page limit. The new self-driving-car sentence is a better hook, but it needs a citation, and it connects nicely to the takeover-prediction work noted under Operator supervision. Use the space for *when and why this became a CS/ML problem* (manual question 4).

## 2. Related Work

Station keeping with a USV is not a new problem.  Many other companies actively research and perform this in different capacities.  

In the following sections we explore some of the most common methods and research done in field.  other reaserch (TTG's paper) explore time to run aground which can be looked as time until vessel crosses the 10nm boundary and the solution is virtually the same.  The paper also argues that distance alone (geofencing) is a weaker warning signal that a time-to-event estimation, accounting for drift.  this is an inspiration or userful reasearch information for our problem

``
Organize existing approaches into meaningful categories and subcategories by: 
- type of algorithm
- information or features used
- type of data
- learning technique

Purpose of this section is to help reader understand existing approaches
``

> **[Claude]** This section needs the **hierarchy figure** (20%). Manual §1.3: pick one perspective for level 1 and one for level 2. Your 2.1/2.2/2.3 split is "what question the method answers" (how to hold position / where it will drift / when a human should act). A level-2 split that works across all three is **physics- or expert-knowledge-based vs. data-driven**, which is also the axis your project sits on. Here's where your linked sources currently fall (check this against your own reading):
>
> | | physics / expert-knowledge | data-driven / hybrid |
> |---|---|---|
> | 2.1 control | Sarda 2016; Qu & Cai 2022 | (none linked) |
> | 2.2 drift | Dugan & Utne 2024 (TTG) | Song et al. 2024 (LEEWAY + FCNN) |
> | 2.3 risk / supervision | Kristensen 2022 (DBN); Li 2024 (FTA-FBN); Na 2025; Chen 2021 (review) | **empty, which is where your project sits** |
>


### 2.1 station keeping control

#### Geofencing
A popular approach is *Geofencing*  - radius threshold - essentially once the USV drifts outside of some geofence - do something.
Geofencing is the most popular approach to station keeping with a USV.  The focus is often centered around energy efficiency, and what are the best methods.  Simple feedback loops are are a common implemnetation to combat different marine weather (winds, currents).  This could encorporate wind sensors, water current sensors, or simply drift COG speed over time of the location.

> - A possible source: Wave Glider spec sheets give a *station-keeping radius* (30 m, met 90% of the time; [Boeing/Liquid Robotics product sheet](https://www.boeing.com/resources/boeingdotcom/defense/autonomous-systems/wave-glider-sharc/wave_glider_product_sheet.pdf)). That is the watch-circle idea, and it's much closer to OOR's 10 nm zone.

Other papers look at feedback closed-loop controllers that hold position (Sarda), while this would be beneficial to employing a autopilot control system which determines commands given the telemetry, this is out of scope for this project.  Though interesting, these papers do not allow for drift and are not framed around energy efficiency, but rather opimize heading and position accuracy.

Though these methods are useful in autonomous piloting, and certain aspects will be useful to consider in our design (such as live telemtry calculating to determine action, considering wind and location as input, general geofencing concepts), our solution aims to reduce human piloting time but not remove it.  

Geofencing limitations ignore when usv is drifting and only act when the usv reaches a limit.  Our solution aims to improve on this by constantly assessing distance.

> - A contrast for the comparison: the control papers work at metres and minutes with no human involved. OOR works at nautical miles and hours, with a pilot.
> - With your framing (improving station-keeping practice), the geofence/watch-circle rule *is* the current practice you're improving on: the pilot acts when the vessel nears 10 nm. Describe it as current practice, give its limitation (it reacts to distance and ignores where the vessel is drifting), and reuse it as your baseline in §3.
> - Geofencing and feedback loops overlap: a geofence is a trigger rule, while a feedback loop is a controller. "Threshold/trigger-based" vs. "continuous feedback control" might work better as the two subcategories.

#### Feedback loops

#### Weather optimal positioning
Another interesting approach to saving energy while geofencing is using Weather Optimal positioning -- which essentially is keeping the USV pointed into the wind to to minimize aerodynamic drag. [Paper](https://www.sciencedirect.com/science/article/pii/S0029801822000725) (another)[https://arxiv.org/pdf/1702.04941]

> **[Claude] Link check:**
> - **"Paper"** is **Qu & Cai, "Nonlinear station keeping control for underactuated unmanned surface vehicles to resist environmental disturbances", Ocean Engineering 246 (2022)**, doi:10.1016/j.oceaneng.2022.110603. It's paywalled, so I only read the abstract. An update law slowly turns the heading until it faces *against the combined disturbance* (unknown magnitude and direction). That's "into the disturbance", not specifically "into the wind to minimise aerodynamic drag", and the abstract doesn't mention energy.
> - **"(another)"** is arXiv 1702.04941, which is **Sarda et al. 2016**: the same paper as `sarda2016station`, already in your proposal bib. It isn't a weather-optimal positioning paper. It compares PD, backstepping and sliding-mode controllers, with and without wind feedforward, on a 4 m, 180 kg WAM-V in 4–5 kn wind. Sliding mode did best, and feedforward only helped PD and backstepping in cross-wind. For a real weather-optimal positioning source, see its ref [53]: Kjerstad et al., "Weather Optimal Positioning Control for Marine Surface Vessels", IFAC CAMS 2010.
> - The markdown link is reversed: `(another)[url]` should be `[another](url)`.

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
> - **Method (physics-based):** drift velocity = sea current + wind/wave-forced drift (the Sørgård & Vada model). Drift direction is modelled as a normal distribution; at sampled angles, distance-to-ground ÷ drift speed gives a time, and the times are combined in a probability-weighted sum.
> - **Data:** ship position, historical forecast wind/wave/current (NorKyst model) and water depth. Demonstrated on one research-ship voyage in Norway. No learning and no real groundings to validate against.
> - **Limitations (their §5.2):** the drift model was only validated on 250–270 m tankers, and it assumes constant weather, so it's less reliable beyond a few hours.

> Replace "ground" with "the 10 nm boundary" and that's close to your problem. It's a strong anchor for both the comparison and the positioning. Your differences: a small USV, learned from logged telemetry, with pilot intervention as the label.

> - "Predictive Drift Models - calculate probability of exceeding boundary in next *t*" isn't what TTG computes: TTG is an expected time, not a probability within a window. Your project is the probability-within-a-window version.

Assessing other work [Drift prediction with a neural-network correction](https://www.mdpi.com/2077-1312/12/12/2262) shows how using ML can greatly improve the accuracy of things like drift prediction, and consequently in our case would improve accuracy of probability in v2.  here is improved "the mean distance between predicted and actual track fell from **5.75 km to 0.41 km*" ~10x improvement in accuracy, using physics, simulations and ML.  Shows the benefit of data driven prediction models.


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

> **[Claude]** This is empty, but your proposal already cites `bogg2026alert` (a visual alert reduced unnecessary human intervention in an automated vehicle), and it belongs here. A related data-driven line of work is driver takeover prediction for self-driving cars. One example is **DeepTake** (Pakdamanian et al., CHI 2021, [arXiv:2012.15441](https://arxiv.org/abs/2012.15441)), which predicts whether and how quickly a driver will respond to a takeover request (96% accuracy on intention). It answers a different question (the driver's *response*, not *whether* intervention is needed), but it's a useful contrast in the table.

Other resources:
[The Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipmen](https://www.mdpi.com/2077-1312/12/12/2262)

[Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships](https://www.mdpi.com/2077-1312/13/5/970)

[Review of Risk analysis](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf)

> **[Claude]** What each "other resource" is:
> - **"Prediction and Dynamic Correction of Drifting Trajectory":** move to 2.2 (see the note there).
> - **"Qualitative Risk Assessment Methodology…":** **Na et al., "Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships: Cognitive Model-Based Functional Analysis and Hazard Identification" (COFA-HAZID), JMSE 13(5):970, 2025** (Korean Register). Design-phase and qualitative, with no numeric risk. It gives you a citable argument for dynamic over static assessment: systems that "drastically reduce human intervention" may require "real-time risk assessment methodologies". It also reports that STPA is the most-used qualitative method for MASS.
> - **"Review of Risk analysis":** **Chen, Bose, Brito, Khan, Thanyamanta & Zou, "A Review of Risk Analysis Research for the Operations of Autonomous Underwater Vehicles", Reliability Engineering & System Safety 216 (2021)** (abstract only; the PDF link blocked me). It reviews 42 papers, sorts methods into qualitative / semi-quantitative / quantitative, and recommends dynamic risk analysis and work on limited historical data. Its taxonomy could be your level-2 split for 2.3, and citing it backs up your hierarchy.
> - **Possibly useful for between 2.1 and 2.2:** Clark et al., "Station-Keeping Underwater Gliders Using a Predictive Ocean Circulation Model and Applications to SWOT Calibration and Validation", IEEE JOE, 2020 ([PDF](https://ai.jpl.nasa.gov/public/papers/clark-joe2019-station.pdf)). It does *predictive* station keeping from an ocean-current forecast, with simulation and field results. I only saw the abstract.




## 3.  Positioning Project - Rowan

Our problem differs in that we want to employ a hybrid method, combining the benefits of these popular techniques.

> **[Claude]** "We want to employ a hybrid method, combining the benefits of these popular techniques" is a positioning claim, so move it to §3. Here, just introduce the categories and the hierarchy figure. If you keep "hybrid", say what's combined: you aren't merging a control law into the model (see overall note 2).

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
> - Keeping this as its own section is fine, but it needs to come *before* Positioning (as 2.4 or section 3), not inside it (overall note 1).
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
