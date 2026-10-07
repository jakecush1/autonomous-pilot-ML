# Predicting Pilot Intervention for Station-Keeping USVs: A Brief Review

>  Reading list (most important first).** 

> **Suggested split, based on the names on your headings:** Jake reads 5 and 6 (history, hierarchy); Rowan reads 1 and 2 (comparison, positioning); you both read 3 and 4.

>  **Sources:** the 10 links are only 8 distinct papers, and several labels don't match the paper (notes at each link). Only one of them, Kristensen et al. 2022 (§2.3), is about *when an operator should pay attention*. That makes it your closest prior work.

> | 1 | **Kristensen, Liu & Utne 2022**, "Dynamic Risk Analysis of Maritime Autonomous Surface Ships", PSAM16. [PDF](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf) | Closest prior work: risk model for a USV with a shore operator checking in every 2 h; suggests the model can tell the operator when to pay attention | **All** (12 pp) | 2.3, comparison, positioning |
> | 2 | **Dugan & Utne 2024**, "Development of a risk indicator for ship drifting groundings", PSAM17. [PDF](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf) | Time-to-event early warning built from drift; argues that distance alone is a weak signal. Replace "ground" with "10 nm boundary" | **All** (10 pp) | 2.2, comparison, positioning |
> | 3 | **Sarda et al. 2016**, "Station-keeping control of a USV exposed to current and wind disturbances", Ocean Eng. 127 (already `sarda2016station`). [arXiv](https://arxiv.org/pdf/1702.04941) | Your representative station-keeping control paper; its §II is a mini-survey of station-keeping control | Abstract, §I–II, conclusions (long paper; skip the maths) | 2.1, comparison |
> | 4 | **Song et al. 2024**, "Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipment…", JMSE 12:2262. [MDPI](https://www.mdpi.com/2077-1312/12/12/2262) | The only data-driven drift paper you have (physics model + neural-network correction) | Abstract, method overview, results, §5 limitations | 2.2, comparison |
> | 5 | **Manley 2008**, "Unmanned surface vehicles, 15 years of development", OCEANS 2008. [link](https://scispace.com/pdf/unmanned-surface-vehicles-15-years-of-development-4nxzuv0wq9.pdf) | The history source; replaces the Wikipedia links | History sections | 1.1 |
> | 6 | **Chen et al. 2021**, "A Review of Risk Analysis Research for the Operations of AUVs", RESS 216. [PDF](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf) | Its qualitative / semi-quantitative / quantitative taxonomy can justify your hierarchy for 2.3 | Abstract + taxonomy section only | 2 overview, 2.3 |
> | 7 | **Qu & Cai 2022**, "Nonlinear station keeping control for underactuated USVs…", Ocean Eng. 246. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0029801822000725) (paywalled; use the UVic library) | A second station-keeping control example (heading turns to face the disturbance) | Abstract + intro | 2.1 |
> | 8 | **Na et al. 2025**, qualitative MASS risk (COFA-HAZID), JMSE 13:970. [MDPI](https://www.mdpi.com/2077-1312/13/5/970) | A one-line citation for "static/design-phase risk isn't enough; real-time assessment is needed" | Abstract + intro | 2.3 |
> | 9 | `bogg2026alert` (already in the proposal bib) | Operator alerting in automated vehicles | Whatever you used for the proposal | 2.3 Operator supervision |
>
> **Optional or new finds:** DeepTake ([arXiv:2012.15441](https://arxiv.org/abs/2012.15441); data-driven takeover prediction in cars), the Wave Glider [product sheet](https://www.boeing.com/resources/boeingdotcom/defense/autonomous-systems/wave-glider-sharc/wave_glider_product_sheet.pdf) (a "watch circle" source for the geofence approach), and Clark et al., IEEE JOE 2020 ([PDF](https://ai.jpl.nasa.gov/public/papers/clark-joe2019-station.pdf); predictive station keeping). **Probably drop:** Li et al. 2024 (the collision FTA-FBN paper behind the "Risk assesment" and "Marine Risk assessment" links), since collision isn't your failure mode.





> 2. **Station-keeping framing (updated):** your framing works: station-keeping literature belongs in the review, and its gaps motivate your system. Be precise about *which part* you improve, though. Your model doesn't issue commands (proposal: it "predicts only whether intervention is required"), so the improvement is to station-keeping *supervision* (when a human must act), not to the *control law* that holds position. The proposal's intro calls control-law work "a different problem", so add one sentence in this document that bridges the two (control = how the vessel holds station; this project = supervising station keeping) so a marker doesn't see a contradiction.


> 4. **Graded items still missing:** abstract, hierarchy figure, comparison table, Venn diagram.


## Abstract -jake

> **[Claude] Ideas for the abstract.** These are points to cover, not wording; this milestone only allows AI-assisted *editing*, so the sentences need to be yours.
> - **Scope statement (1 sentence):** what this paper is, e.g. a brief review of the history and current state of [deciding when a station-keeping USV needs a human pilot]. The example's abstract is essentially just this sentence.
> - **Context (1 clause):** OOR's DataXplorer holds within 10 nm of a retired NOAA buoy station, with a pilot on 24/7 watch.
> - **What the review covers:** the history (your timeline, from early roots to autonomous USVs), then the three families: station-keeping control, drift prediction, and risk assessment & operator supervision. Optionally name your level-2 split (physics/expert-based vs. data-driven).
> - **The main takeaway:** control methods hold position but don't say when a human is needed. Drift/TTG and dynamic-risk methods give early warnings but are physics- or expert-based and were validated on single voyages or missions. None learns *when the pilot is needed* from telemetry.
> - **Where you fit:** a data-driven model that predicts pilot intervention within a time window, building on time-to-event (TTG) and dynamic-risk ideas, compared against a distance-threshold baseline.
> - **Repository link (required):** manual §1.6.2 says the repo must be linked in the abstract. Your proposal abstract already has the sentence with https://github.com/jakecush1/autonomous-pilot-ML, so reuse it.
> - **Length:** with exactly 2 pages, aim for 3–5 sentences plus the repo sentence. Write it last, once the sections are settled.
> - **Keywords line** (the example template has `\keywords{}`; pick about 4): unmanned surface vehicles, station keeping, human-in-the-loop, dynamic risk assessment, drift prediction.

## 1. Introduction - Both read and research
Our problem is exploring the idea of "if we can determine *When* a human interaction is needed, while station keeping with a USV".  In exploring this topic we found it import to first explore the most popular methods of station keeping used in the industry.

- what approaches have been used to address OUR problem: while station keeping with a USV, when is human interaction needed?

Here is our specific problem at the company. we care because - having to pay someone is expensive

some approaches to solving this problem are x, y z, and their shortcomings are a,b,c.
  - method 1 does a well but not b, method 2 does b well but not c; our method will take pros from 1 and 2 and do a, b and c

3 methods used in automated marine station keeping, and USV station keeping which are relevant to our problem.  These are current popular methods which are researched, simulated, tested and used.  Ideally our method or solution would combine all of these methods, considering all research and creating a probability rating which considers geofencing and usv location relative to its station, calcualtes a drift prediction based on current telemetry, and considers other data to influence the probabilty encompassing risk assessment.

> **[Claude]** The "some approaches… x, y z" lines are a good skeleton for the four questions in manual §1.1. The "3 methods used…" paragraph is mostly positioning ("Ideally our method…"), so move it to §3. "Researched, simulated, tested and used" needs citations showing which papers did which; the comparison table can carry that.

### 1.1 History - jake

origin and evolution of the problem, context for those not familiar. where the problem came from, why its important to CS and ML trace problem back to its eariliest roots, even before CS. earliest ideas, practices or challenges that are related to the problem 
- do not give exhaustive history, give quick journey from early origins to modern

" early forms of weather reporting we done by .... later they used radio, now its all online...
"early marine navigation decisions done by ... captains? ... now done by robots with pilots.... 
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
> - The manual asks for the earliest roots of the *problem*. The example starts from the problem itself (1927 voting blocs), not the technology. Your timeline is a history of unmanned boats, but the proposal's problem is *keeping a vessel on station and knowing when a human needs to step in*. Your notes on weather reporting and captains' decisions are closer to that root. Consider leading with them, then the remote-control timeline, then where ML enters.
> - "1914: WW1 - german army…": the Fernlenkboote were built for the Imperial German *Navy*, not the army, and I believe they were used in combat around 1916–17. Check "1914".
> - "1940s - 1990s" covers 50 years. The "USV Development last 15 year" paper is the source to split it up.
> - "1990-2010": Saildrone was founded in 2012, which is outside that range.
> - "USV Development last 15 year" is **Manley, J., "Unmanned surface vehicles, 15 years of development", MTS/IEEE OCEANS 2008** (doi:10.1109/OCEANS.2008.5152052). It's ref [1] in Sarda et al. Cite it instead of the Wikipedia links; the manual asks for textbooks, surveys, influential papers or reliable technical sources. (scispace blocked me, so I haven't read the body.)
> - "Most people think humanoid…" is off-topic for a 2-page limit. The new self-driving-car sentence is a better hook, but it needs a citation, and it connects nicely to the takeover-prediction work noted under Operator supervision. Use the space for *when and why this became a CS/ML problem* (manual question 4).

## 2. Related Work

Station keeping with a USV is not a new problem.  Many other companies actively research and perform this in different capacities.  Our problem differs in that we want to employ a hybrid method, combining the benefits of these popular techniques.

In the following sections we explore some of the most common methods and research done in field.  other reaserch explore time to run aground, where this is not a concern for us.

> **[Claude]** "We want to employ a hybrid method, combining the benefits of these popular techniques" is a positioning claim, so move it to §3. Here, just introduce the categories and the hierarchy figure. If you keep "hybrid", say what's combined: you aren't merging a control law into the model (see overall note 2).
>
> On "time to run aground… not a concern for us": grounding itself isn't your risk, but the TTG paper's *idea* carries over directly. Replace "time until the vessel hits ground" with "time until it crosses the 10 nm boundary". The paper also argues that distance alone (the geofence view) is a weaker warning signal than a time-to-event estimate that accounts for drift. I'd cite it as inspiration rather than dismiss it.

Organize existing approaches into meaningful categories and subcategories by: 
- type of algorithm
- information or features used
- type of data
- learning technique

Purpose of this section is to help reader understand existing approaches

> **[Claude]** This section needs the **hierarchy figure** (20%). Manual §1.3: pick one perspective for level 1 and one for level 2. Your 2.1/2.2/2.3 split is "what question the method answers" (how to hold position / where it will drift / when a human should act). A level-2 split that works across all three is **physics- or expert-knowledge-based vs. data-driven**, which is also the axis your project sits on. Here's where your linked sources currently fall (check this against your own reading):
>
> | | physics / expert-knowledge | data-driven / hybrid |
> |---|---|---|
> | 2.1 control | Sarda 2016; Qu & Cai 2022 | (none linked) |
> | 2.2 drift | Dugan & Utne 2024 (TTG) | Song et al. 2024 (LEEWAY + FCNN) |
> | 2.3 risk / supervision | Kristensen 2022 (DBN); Li 2024 (FTA-FBN); Na 2025; Chen 2021 (review) | **empty, which is where your project sits** |
>
> The empty bottom-right cell lets you show your position without claiming to do everything.

### 2.1 station keeping control

#### Geofencing
A popular approach is *Geofencing*  - radius threshold - essentially once the USV drifts outside of some geofence - do something.
Geofencing is the most popular approach to station keeping with a USV.  The focus is often centered around energy efficiency, and what are the best methods.  Simple feedback loops are are a common implemnetation to combat different marine weather (winds, currents).  This could encorporate wind sensors, water current sensors, or simply drift COG speed over time of the location.

> **[Claude]** The geofencing claims here have no source, and the two control papers you linked don't support them. Both are *continuous* closed-loop controllers that hold position to within metres over minutes (Sarda tested in 4–5 kn wind). Neither waits for the vessel to drift out and then reacts, and neither is framed around energy efficiency (Sarda optimises heading and position accuracy). Either find a geofence / "watch circle" source or reframe this paragraph.
> - A possible source: Wave Glider spec sheets give a *station-keeping radius* (30 m, met 90% of the time; [Boeing/Liquid Robotics product sheet](https://www.boeing.com/resources/boeingdotcom/defense/autonomous-systems/wave-glider-sharc/wave_glider_product_sheet.pdf)). That is the watch-circle idea, and it's much closer to OOR's 10 nm zone.
> - A contrast for the comparison: the control papers work at metres and minutes with no human involved. OOR works at nautical miles and hours, with a pilot.
> - With your framing (improving station-keeping practice), the geofence/watch-circle rule *is* the current practice you're improving on: the pilot acts when the vessel nears 10 nm. Describe it as current practice, give its limitation (it reacts to distance and ignores where the vessel is drifting), and reuse it as your baseline in §3.
> - Geofencing and feedback loops overlap: a geofence is a trigger rule, while a feedback loop is a controller. "Threshold/trigger-based" vs. "continuous feedback control" might work better as the two subcategories.

#### Feedback loops

#### Weather optimal positioning
Another interesting approach to saving energy while geofencing is using Weather Optimal positioning -- which essentially is keeping the USV pointed into the wind to to minimize aerodynamic drag. [Paper](https://www.sciencedirect.com/science/article/pii/S0029801822000725) (another)[https://arxiv.org/pdf/1702.04941]

> **[Claude] Link check:**
> - **"Paper"** is **Qu & Cai, "Nonlinear station keeping control for underactuated unmanned surface vehicles to resist environmental disturbances", Ocean Engineering 246 (2022)**, doi:10.1016/j.oceaneng.2022.110603. It's paywalled, so I only read the abstract. An update law slowly turns the heading until it faces *against the combined disturbance* (unknown magnitude and direction). That's "into the disturbance", not specifically "into the wind to minimise aerodynamic drag", and the abstract doesn't mention energy.
> - **"(another)"** is arXiv 1702.04941, which is **Sarda et al. 2016**: the same paper as the "Station-Keeping USV" ResearchGate link under Other resources, and `sarda2016station`, already in your proposal bib. It isn't a weather-optimal positioning paper. It compares PD, backstepping and sliding-mode controllers, with and without wind feedforward, on a 4 m, 180 kg WAM-V in 4–5 kn wind. Sliding mode did best, and feedforward only helped PD and backstepping in cross-wind. For a real weather-optimal positioning source, see its ref [53]: Kjerstad et al., "Weather Optimal Positioning Control for Marine Surface Vessels", IFAC CAMS 2010.
> - The markdown link is reversed: `(another)[url]` should be `[another](url)`.

### 2.2 Drift prediction
Another similar algorithm would be drift prediction:
Predictive Drift Models - calculate probability of exceeding boundary in next *t* time:
Drift prediction Algorithm looks similar to "Drifting Grounding" Algorithms - [Development of Risk indicator for ship drifting - Monte Carlo](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf)

> **[Claude]** Read in full: **Dugan & Utne, "Development of a risk indicator for ship drifting groundings", PSAM17 & ASRAM 2024 (NTNU).** It does **not** use Monte Carlo, so fix the label.
> - **Output:** *time to grounding* (TTG), the expected time until a ship that loses propulsion would drift aground. It's recomputed along the voyage as an early warning.
> - **Method (physics-based):** drift velocity = sea current + wind/wave-forced drift (the Sørgård & Vada model). Drift direction is modelled as a normal distribution; at sampled angles, distance-to-ground ÷ drift speed gives a time, and the times are combined in a probability-weighted sum.
> - **Data:** ship position, historical forecast wind/wave/current (NorKyst model) and water depth. Demonstrated on one research-ship voyage in Norway. No learning and no real groundings to validate against.
> - **Limitations (their §5.2):** the drift model was only validated on 250–270 m tankers, and it assumes constant weather, so it's less reliable beyond a few hours.
> - **Why it matters to you:** their main argument is that *distance to shore* (what geofence-style systems use) is a worse risk signal than TTG because it ignores drift. Replace "ground" with "the 10 nm boundary" and that's close to your problem. It's a strong anchor for both the comparison and the positioning. Your differences: a small USV, learned from logged telemetry, with pilot intervention as the label.
> - "Predictive Drift Models - calculate probability of exceeding boundary in next *t*" isn't what TTG computes: TTG is an expected time, not a probability within a window. Your project is the probability-within-a-window version.
>
> **The "Prediction and Dynamic Correction of Drifting Trajectory" link under Other resources also belongs here:** **Song et al., "The Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipment Based on Fully Connected Neural Network (FCNN) Embedding Model", JMSE 12(12):2262, 2024.** It's a hybrid: the US Coast Guard LEEWAY physics model predicts the drift trajectory, and an FCNN corrects it using the drifting object's own position reports. In sea trials, mean deviation fell from 5.75 km to 0.41 km. Limitations: it's for *unpowered* lost equipment (search and rescue), it ignores waves, and it depends on interpolated forecast wind and current. It's your best example of data-driven drift prediction.

### 2.3 Dynamic Risk assessment & supervision
#### DRA
Consider other risks, DRA, opertator alerting systems, forecast consideration?
- Dynamic Risk Assessment (DRA): [Risk assesment](https://www.sciencedirect.com/science/article/pii/S0029801824017827)
- [Dynamic Risk Assessment](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf)

> **[Claude] Link check:**
> - **The "Risk assesment" link** (the same URL as "Marine Risk assessment" under Other resources) is **not** a dynamic risk paper. It's **Li, Wang & Yang, "Risk assessment of maritime autonomous surface ships collisions using an FTA-FBN model", Ocean Engineering 309 (2024)**. It covers *collision* risk: a fault tree mapped into a fuzzy Bayesian network, with probabilities from expert surveys because MASS failure data is scarce. It's static and design-level, not real-time. It could serve as the "static, expert-elicited" example in 2.3, or you could drop it, since collision isn't your failure mode. Open-access copy: [LJMU repository](https://researchonline.ljmu.ac.uk/id/eprint/24721/).
> - **The "Dynamic Risk Assessment" (PSAM16) link is your most important paper.** I read it in full: **Kristensen, Liu & Utne, "Dynamic Risk Analysis of Maritime Autonomous Surface Ships", PSAM16 2022.**
>   - A dynamic Bayesian network (DBN) estimates mission-failure risk from power management and situation awareness on a 5 m AutoNaut USV (wave-propelled, solar-powered).
>   - Case study: a 19-day mission off Norway, operating within a defined area. A shore operator checked in **every 2 hours**, which is also the DBN's time step. That's very close to OOR's pilot cadence. The real vessel grounded in a storm after losing communications with a low battery, and the model's risk rose before the event.
>   - Its probability tables come from system data plus expert judgement, and it was validated only by sensitivity analysis on that one mission.
>   - The authors say the model "can also give indications for when the human operator on shore should pay more attention". That's essentially your problem, so the claim in "Identified Gap in the Literature" needs softening. The idea already exists. What's missing is learning it from telemetry, applying it to position/boundary risk, and validating it against real intervention outcomes.

#### Operator supervision

> **[Claude]** This is empty, but your proposal already cites `bogg2026alert` (a visual alert reduced unnecessary human intervention in an automated vehicle), and it belongs here. A related data-driven line of work is driver takeover prediction for self-driving cars. One example is **DeepTake** (Pakdamanian et al., CHI 2021, [arXiv:2012.15441](https://arxiv.org/abs/2012.15441)), which predicts whether and how quickly a driver will respond to a takeover request (96% accuracy on intention). It answers a different question (the driver's *response*, not *whether* intervention is needed), but it's a useful contrast in the table.

Other resources:
[The Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipmen](https://www.mdpi.com/2077-1312/12/12/2262)

[Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships](https://www.mdpi.com/2077-1312/13/5/970)

[Marine Risk assessment](https://www.sciencedirect.com/science/article/pii/S0029801824017827)

[Review of Risk analysis](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf)

[Station-Keeping USV](https://www.researchgate.net/publication/309185307_Station-keeping_control_of_an_unmanned_surface_vehicle_exposed_to_current_and_wind_disturbances)

> **[Claude]** What each "other resource" is:
> - **"Prediction and Dynamic Correction of Drifting Trajectory":** move to 2.2 (see the note there).
> - **"Qualitative Risk Assessment Methodology…":** **Na et al., "Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships: Cognitive Model-Based Functional Analysis and Hazard Identification" (COFA-HAZID), JMSE 13(5):970, 2025** (Korean Register). Design-phase and qualitative, with no numeric risk. It gives you a citable argument for dynamic over static assessment: systems that "drastically reduce human intervention" may require "real-time risk assessment methodologies". It also reports that STPA is the most-used qualitative method for MASS.
> - **"Marine Risk assessment":** duplicate of the "Risk assesment" link in 2.3 (Li et al. 2024, collision).
> - **"Review of Risk analysis":** **Chen, Bose, Brito, Khan, Thanyamanta & Zou, "A Review of Risk Analysis Research for the Operations of Autonomous Underwater Vehicles", Reliability Engineering & System Safety 216 (2021)** (abstract only; the PDF link blocked me). It reviews 42 papers, sorts methods into qualitative / semi-quantitative / quantitative, and recommends dynamic risk analysis and work on limited historical data. Its taxonomy could be your level-2 split for 2.3, and citing it backs up your hierarchy.
> - **"Station-Keeping USV":** duplicate of the "(another)" arXiv link in 2.1 (Sarda et al. 2016).
> - **Possibly useful for between 2.1 and 2.2:** Clark et al., "Station-Keeping Underwater Gliders Using a Predictive Ocean Circulation Model and Applications to SWOT Calibration and Validation", IEEE JOE, 2020 ([PDF](https://ai.jpl.nasa.gov/public/papers/clark-joe2019-station.pdf)). It does *predictive* station keeping from an ocean-current forecast, with simulation and field results. I only saw the abstract.






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
