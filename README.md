# Predicting Remote Intervention for a Station-Keeping USV

Predict, from live telemetry, whether a remote pilot will need to intervene with an uncrewed surface vehicle (USV) within a future time horizon, so the pilot can be alerted on demand instead of kept on continuous watch.

Course project for SENG 474, University of Victoria.

## Background

Open Ocean Robotics (OOR) operates the DataXplorer, a USV that reports marine weather data for NOAA in place of the discontinued Station 46012 buoy. The vessel's only hard operating constraint is to remain within 10 nautical miles (nm) of the buoy's former position.

A remote pilot currently watches the vessel 24/7, roughly 1,095 eight-hour shifts per year, even though a corrective navigation command is needed only every two to three hours. This project asks whether that decision can be predicted from telemetry, turning a continuous watch into an on-call, alert-driven one.

The model is **advisory only**. It decides *whether* a pilot is needed, never *what* the pilot should do, and all navigation decisions stay with a human.

## Problem Definition

Let $p_0$ be the station point and $p$ the vehicle's reported position, each a latitude–longitude pair. Local wind is given by speed $v \ge 0$ (knots) and direction $\theta \in [0^\circ, 360^\circ)$, measured clockwise from true North as the direction the wind blows *from*.

A state is $\mathbf{s} = (p, p_0, v, \theta)$. Let $d(\mathbf{s})$ be the geodesic distance from $p$ to $p_0$; the operating constraint is $d(\mathbf{s}) \le R = 10$ nm.

For a horizon $\Delta t > 0$, the goal is a decision function

$$f: \mathcal{S} \rightarrow \{0, 1\}$$

where $f(\mathbf{s}) = 1$ if a pilot must issue a corrective command within $[t, t + \Delta t]$ to keep the vehicle inside $R$, and $0$ otherwise.

## Approach

**V1: Expert-labelled decision grid (baseline).** The 10 nm operational area is divided into distance rings and sectors, and wind into direction sectors and speed bands. Each combination is labelled 0 (safe) or 1 (intervention needed) from the rules experienced pilots already use, generated in code and hand-reviewed at the borderline cells. This is a lookup table rather than a trained model, and every later version must beat it.

**V2: Learned intervention probability.** Replace hand labels with observed outcomes from simulation and logged pilot interventions to estimate $\mathbb{P}(Y = 1 \mid \mathbf{s})$, recovering the binary decision by threshold so the alert rate can be tuned without retraining. Planned progression: per-cell frequencies, then logistic regression, then gradient-boosted trees if needed.

**Out of scope:** reinforcement learning for direct navigation control. A V2 model could later serve as a safety monitor for such an agent.

Additional reported measurements (wave height, air and water temperature, depth) are retained as candidate features to be tested for predictive value rather than assumed informative.

## Evaluation

Each version is compared against the V1 grid on:

- **Interventions caught:** the fraction of real interventions the model alerts on in advance (recall).
- **Unnecessary alerts:** false alerts raised per shift.
- **Watch time removed:** hours of continuous monitoring the alert system replaces.

Errors are asymmetric. A missed intervention risks the station-keeping constraint, while a false alert costs one page, so recall on real interventions is weighted above alert precision.

## Repository Layout

Planned structure, to be filled in as milestones progress:

```
autonomous-pilot-ML/
├── docs/          # proposal (LaTeX source + PDF) and milestone reports
├── data/          # gitignored; raw and processed telemetry
├── src/
│   ├── grid/      # V1 expert-labelled decision grid
│   ├── models/    # V2 learned models
│   └── eval/      # evaluation metrics and baselines
├── notebooks/     # exploration and analysis
└── tests/
```

Raw DataXplorer telemetry is not committed to this repository.

## Installation

```bash
git clone https://github.com/jakecush1/autonomous-pilot-ML.git
cd autonomous-pilot-ML
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Execution instructions will be added alongside the V1 grid implementation.

## Milestones

- [x] Project proposal
- [ ] V1 expert-labelled decision grid
- [ ] Simulation and logged-intervention dataset
- [ ] V2 learned models
- [ ] Evaluation against the V1 baseline
- [ ] Final report

## Team

- Jake Cushway, University of Victoria
- Rowan Hall, University of Victoria

Individual contributions are tracked through assigned issues and commit history in this repository.

## License

Released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).