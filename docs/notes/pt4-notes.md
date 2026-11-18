Evaluation strategy
investigates:
- Does the proposed approach achieve satisfactory classification performance?
- Does it outperform conventional classification models?
- How sensitive is its performance to different hyperparameter settings?
- Does it perform consistently across different datasets or experimental configurations?


Model created by NOAA to predict drift and disruption of Oil spills.

Abstract
DataXplorer is a USV that operates 20nm offshore near Half Moon Bay califonrnia.  It acts as a weather station for marine astrological weather, and must stay within a 10nm of the retired NOAA weather buoys location.  The data is publicly available through NOAA, and collected by Open Ocean Robotics.  Code and related documents are available at https://github.com/jakecush1/autonomous-pilot-ML.

Intro
Using curent and past data we attempted to predict drift of the vessel, giving location in 1 hour using 4 ML models: persistence, linear regression, LSTM, transformer. We had data to train the odels, and then unseen data to test these models.  Using a baseline of past drift = future drift.  If we could improve upon this assumption it would be considered progress, then evaulating the predictions against actual data points, to validate them.


Research questions:

Is wind the main proponent of vessel drift in our sample ocean location?

How accurately can we predict drift, given the parameters of the project?
  - past and current data: wind speed, wind direction, location points

Which ML technique will work best for this prediction model?

How are these techniques different than current prediction models?


Dataset
- collected data from past usv drift data.



