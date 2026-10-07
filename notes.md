> | 1 | **Kristensen, Liu & Utne 2022**, "Dynamic Risk Analysis of Maritime Autonomous Surface Ships", PSAM16. [PDF](https://www.iapsam.org/PSAM16/papers/SU247-PSAM16.pdf) | Closest prior work: risk model for a USV with a shore operator checking in every 2 h; suggests the model can tell the operator when to pay attention | **All** (12 pp) | 2.3, comparison, positioning |

risk assessment, considering power consumption vs situational awareness (SA) in marine autnomous surface ships (MASS) using a dynamic Bayesian belief network (DBN) model
- improved SA increases power consumption
- decreasing the level of autonomy (LOA) can increase the risk
- MASS may operate with or dependent or independent on human operators
- the RA takes external factors and determines a probability of mission success/failure

- We can get inspiration of their framework of calculating risk by external factors by using a bayesian network or a DBN.  Though different factors, similar idea. we also want to output a probability based on input telemetry.  Their calculation is more complex than our intiial model

Pros:
- very in depth risk calculation
- works well for conserving power
- 

Cons:
- does not consider relative location keep, or station keeping
- designed for a mission path
- uses wave-foil porpulsion
- uses human operators, we want hybrid monitoring
