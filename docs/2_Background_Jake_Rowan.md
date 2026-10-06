# Seng 474 Background

## Introduction - Both read and research
- what approaches have been used to address this problem: station keeping with a USV, when is human interaction needed
- how are they different

Research USV station keeping methods

A popular approach is *Geofencing* or *virtual Anchor* - radius threshold
- essentially once the USV drifts outside of some geofence - do something

Another similar algorithm would be drift prediction:
Drift prediction Algorithm looks similar to "Drifting Grounding" Algorithms - [Development of Risk indicator for ship drifting - Monte Carlo](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf)

Predictive Drift Models - calculate probability of exceeding boundary in next *t* time 
- Dynamic Risk Assessment (DRA): [Risk assesment](https://www.sciencedirect.com/science/article/pii/S0029801824017827)
- [Dynamic Risk Assessment](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf)


Other resources:
[The Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipmen](https://www.mdpi.com/2077-1312/12/12/2262)

[Qualitative Risk Assessment Methodology for Maritime Autonomous Surface Ships](https://www.mdpi.com/2077-1312/13/5/970)

[Marine Risk assessment](https://www.sciencedirect.com/science/article/pii/S0029801824017827)

[Review of Risk analysis](https://eprints.soton.ac.uk/id/eprint/451143/1/A_Review_of_Risk_Analysis_Research_for_the_Operation_of_Autonomous_Underwater_Vehicles_revised_13th_Jan_no_markup_rev1.pdf)

[Station-Keeping USV](https://www.researchgate.net/publication/309185307_Station-keeping_control_of_an_unmanned_surface_vehicle_exposed_to_current_and_wind_disturbances)



## history - jake
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

USV's have been in development for over 100 years, but the ability for them to be driven autonomously is a relatively new concept.  This topic of autonomous driving, humanless piloting, is popular and new.  Autonomous Robotics is a huge topic in ML and CS.  Most people think humanoid, but the development of autonomous piloting and robotics development are all closely related.

## Hierarchy - Jake
Organize existing approaches into meaningful categories and subcategories by: 
- type of algorithm
- information or features used
- type of data
- learning technique

Purpose of this section is to help reader understand existing approaches

## Comparative analysis - Rowan

#### Existing Approaches and Their Limitations
Existing  solutions  fall into reactive control or model based trajectory estimators. While reactive geofences are computationally light, they are inherently backward-looking—initiating counter-thrust only after a vessel has drifted outside its designated boundary. This leads to excessive power consumption and increased risk of grounding in strong, dynamic currents. Conversely, physics-based predictive drift models and Dynamic Risk Assessment (DRA) frameworks offer proactive safety boundaries but heavily rely on explicit dynamic oceanographic models that are difficult to calibrate in real time.

#### Identified Gap in the Literature
Most current frameworks treat station-keeping as a deterministic control problem or rely on static risk thresholds. There is a clear gap in utilizing [insert your ML focus here, e.g., historical trajectory data mining / probabilistic machine learning / Dynamic Risk Indicators] to predict drift probability dynamically under stochastic marine conditions before a boundary breach occurs. Furthermore, existing literature lacks a clear integration between dynamic risk scoring and automated human-intervention triggers.

### Positioning Project

1. propose a data driven model that mines historical telemetry (GPS, wind, current vectors) to predict boundary exceedance $t$ seconds into the future.
2.Real time risk scoring shifts operations from reactive thrusting to early, power-efficient drift mitigation.
3. **Human Integration:** Clear thresholds define when the system operates autonomously vs when human pilot.