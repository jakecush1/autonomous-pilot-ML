> | 9 | `bogg2026alert` (already in the proposal bib) | Operator alerting in automated vehicles | Whatever you used for the proposal | 2.3 Operator supervision |

> [Claude] Written by Claude from the full paper (10 pp, open access: [PDF](https://openaccess-api.cms-conferences.org/articles/download/978-1-964867-76-2_65)). These aren't your own notes, so check them against the paper before using them in the review.

A human factors study of remote operators supervising several self-driving cars: does a "risk" alert change when they intervene? Without the alert they intervened *more*, including when no help was needed.

- **Citation:** Bogg & Birrell, "Do Not Adjust Your Set! How a Visual Alert Reduced Unnecessary Human Intervention in an Automated Vehicle", IHSI 2026 (AHFE vol. 200), pp. 657–666. Coventry University. doi:10.54941/ahfe1007124.
- **Goal:** design advice for remote-operator interfaces (HMI), as part of a larger study on how many AVs one person can monitor.
- **Setup:**
  - 24 participants role-played a remote operator in a simulated control centre, watching fleets of 3, 5, 7 and 9 AVs (video feeds), 15 minutes per fleet size.
  - The AVs sometimes stopped (about 20 s on average). "Call Dilemmas" were longer stops (about 51 s) designed to tempt an intervention, roughly one per 10 min per AV.
  - The HMI showed a coloured border (green/amber/red "risk"), a text reason (e.g. "Stopped In Congestion - Possible Assistance Needed"), a stopwatch of time stopped, and the video. The amber alert meant "stopped for 10 s or more".
  - The manipulation: in each trial, one late event had **no** amber alert.
- **Results:**
  - Without the alert, people intervened **more**. That held for events meant to tempt them (Z = −2.858, p = .004) and for distractors that needed no help (Z = −3.166, p = .002).
  - The longer a vehicle sat still, the more likely people were to intervene (r = .828), whether it needed help or not.
  - The text message mattered most. If the AV asked for help, people gave it 92% of the time; if it didn't ask, 94% of people didn't intervene.
- **Explanation:** "action bias" and the Zeigarnik effect, where an unresolved situation creates pressure to act. A status alert reassures the operator that "inaction can be an appropriate and system-approved response".
- **Caveat from the authors:** the alert is "a double-edged sword". It reduced unnecessary interventions, but it also reduced some of the wanted ones.
- **Future work:** how alert timing affects decisions, and more detailed alert categories.

- Link to us: we're building the alert. Pilots act on what the system tells them, so false alerts and missed alerts both matter. Showing an "all OK" status as well as alerts might stop pilots from stepping in when they don't need to.

Pros:
- A real experiment with statistics, and very recent (2026).
- Directly about when a remote human intervenes, and how information from the system changes that.
- Supports giving the pilot a probability or status, not only an alarm.

Cons:
- Road vehicles with events lasting seconds; ours last hours.
- A lab simulation using video playback, not real operations.
- Studies how the human responds to an alert, not how to predict when one is needed.

> **[Claude] Differences to our situation** (could become a row in your comparison table):
>
> | | Bogg & Birrell 2026 | Our project |
> |---|---|---|
> | Vehicle | Simulated automated road vehicles (fleets of 3–9) | One OOR DataXplorer |
> | Question | How does an alert change the operator's decision to intervene? | When does the pilot need to act? |
> | Alert | Amber border after 10 s stopped, plus a text reason | Alert when P(intervention within Δt) passes a threshold |
> | Timescale | Seconds | Hours |
> | Data | Lab study, 24 participants | Telemetry + logged pilot interventions |
> | Human role | Remote monitor hands stuck AVs to another operator | Pilot moves from 24/7 watch to on-call alerts |
>
> **Where it goes in the background doc:** 2.3 Operator supervision (the proposal intro already cites it). In Positioning, our model produces the kind of alert this HMI depends on, and this paper is a reason to tune the threshold for false alerts, not only for recall.
