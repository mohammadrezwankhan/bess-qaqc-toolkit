# Parameters and symbols

[Handbook](../INDEX.md) · [Equations](EQUATIONS_AND_DERIVATIONS.md) · [Limits](ASSUMPTIONS_AND_LIMITS.md)

The meanings here are local to `bess-qaqc-toolkit` at source revision `af44c932684dfd120dea05d150cefcc3e47539a0`. Display labels do not rename the exported JavaScript keys.

## Active workload lesson

| Symbol | Code key or derived value | Meaning and unit | Configured UI default | Bounds / step |
|---|---|---|---|---|
| $\lambda$ | `alertRate` | Incoming findings, findings/min | 12 | 2–60 / 1 |
| $n$ | `analystCount` | Evidence reviewers, people | 2 | 1–12 / 1 |
| $\mu$ | `reviewRate` | Per-reviewer capacity, findings/min/person | 4 | 1–10 / 0.5 |
| $a$ | `automationPct` | Assumed correct clerical triage, percent | 0 | 0–90 / 5 |
| $t$ | `time` argument | Elapsed minutes | User-selected within lesson | 0–60 |
| $d$ | `manual` local | Remaining manual incoming rate, findings/min | Derived | $\lambda(1-a/100)$ |
| $c$ | `capacity` local | Aggregate manual capacity, findings/min | Derived | $n\mu$ |
| $B$ | `backlog` | Unreviewed findings, count | Derived | Nonnegative fluid count |
| $C$ | `coveragePct` | Nominal incoming-rate coverage, percent | Derived | Capped at 100 |
| $R$ | `reviewedAlerts` | Automatically plus manually processed findings, count | Derived | Accumulated from zero |
| $U$ | `workloadPct` | Reviewer utilization, percent | Derived | Capped at 100 |

Configuration: [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L54-L144). Implementation: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L305-L308).

These are fictional teaching inputs. No field dataset, measured arrival distribution, reviewer-time study, or fitted parameter source is supplied for this lesson. Counts are continuous fluid quantities; the model does not enforce integer jobs or reviewers for direct API calls.

### UI defaults and engine defaults differ

The `security` engine specification retains generic defaults `(20,4,4,35)` for `(alertRate,analystCount,reviewRate,automationPct)`. The selected lesson explicitly supplies `(12,2,4,0)` and relabels alerts as findings. Calling `resolveParameters("security", {})` therefore does not reproduce the initial configured lesson. Use the configured defaults or a module preset when reproducing screenshots and checkpoints. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L216-L222) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L235-L242) [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L54-L99)

The engine clamps finite numeric values to bounds and uses engine defaults for other inputs. It does not coerce numeric strings or round to slider steps. Bounds are teaching controls, not validated operating limits for a plant or a team.

## Native record and policy quantities

| Quantity | Representation | Meaning / convention | Source |
|---|---|---|---|
| Assessment date | ISO date `YYYY-MM-DD` | Explicit calendar date for deterministic evaluation; no wall-clock dependence in the supplied value | [scripts/audit_deadlines.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_deadlines.py#L58-L65) |
| Due-date difference | Integer days | Due date minus assessment date; negative is overdue | [scripts/audit_deadlines.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_deadlines.py#L78-L180) |
| Calibration interval | Two ISO dates | Inclusive beginning and end; overlapping histories are findings | [scripts/audit_calibration_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_calibration_traceability.py#L236-L553) |
| Status | Normalized text | Meaning comes from the selected policy, not a numeric score | [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L279-L312) |
| Evidence / check / instrument IDs | Controlled text identifiers | Record keys and references; not measurements | [scripts/audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_evidence_traceability.py#L208-L393) |
| Document revision | Numeric or alphabetic sequence | Ordering within one scheme for each document; not software SemVer | [scripts/audit_document_control.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_document_control.py#L149-L157) |
| Issue / record count | Nonnegative integer | Number of parsed records or reported findings in the selected files | [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240) |

Policy files supply controlled vocabulary and acceptance predicates. They do not supply material properties, safety factors, sensor uncertainty, electrical test limits, or statutory requirements. The owner must control those project-specific inputs through the actual engineering assurance process. The example policies are linked in the [interface guide](../developer/API_CLI_AND_INTERFACES.md).

## Shared engine parameter inventory

The following tables enumerate the parameter declarations in all ten callable branches. They report **engine defaults**, not necessarily the active lesson defaults. The branches' source-declared units are preserved. Numeric bounds prevent some invalid arithmetic but are not calibration ranges. No other branch is selected by this repository's current lesson configuration.

### battery

Time unit: h. Evaluation horizon: 6. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L160-L166).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `capacityAh` | Pack capacity | Ah | 20 | 200 | 5 | 100 |
| `currentA` | Discharge current | A | 0 | 30 | 1 | 12 |
| `resistanceOhm` | Internal resistance | Ω | 0.005 | 0.1 | 0.005 | 0.035 |
| `ambientC` | Ambient temperature | °C | 0 | 45 | 1 | 25 |
| `initialSoc` | Initial charge | % | 30 | 100 | 5 | 90 |

### thermal

Time unit: min. Evaluation horizon: 60. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L167-L173).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `heatW` | Heat input | W | 100 | 3000 | 100 | 1200 |
| `coolingWK` | Heat transfer | W/K | 10 | 120 | 5 | 40 |
| `capacityJPerK` | Thermal capacity | J/K | 3000 | 60000 | 1000 | 18000 |
| `ambientC` | Ambient temperature | °C | 0 | 45 | 1 | 25 |

### degradation

Time unit: cycles. Evaluation horizon: 1000. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L174-L180).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `fadePer1000Pct` | Base fade coefficient | % / 1k cycles | 2 | 40 | 1 | 18 |
| `temperatureC` | Cell temperature | °C | 10 | 50 | 1 | 25 |
| `cRate` | Cycling rate | C | 0.2 | 3 | 0.1 | 1 |
| `initialCapacityAh` | Initial capacity | Ah | 10 | 200 | 5 | 100 |

### grid

Time unit: h. Evaluation horizon: 24. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L181-L187).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `demandKW` | Demand baseline | kW | 100 | 1200 | 25 | 500 |
| `solarKW` | Solar peak | kW | 0 | 1400 | 25 | 600 |
| `batteryKW` | Battery discharge | kW | 0 | 300 | 10 | 100 |
| `carbonGPerKWh` | Grid carbon factor | g/kWh | 0 | 800 | 25 | 400 |

### cooling

Time unit: min. Evaluation horizon: 60. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L188-L194).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `serverCount` | Server count | servers | 10 | 500 | 10 | 100 |
| `utilizationPct` | Compute utilization | % | 10 | 90 | 5 | 65 |
| `ambientC` | Outside temperature | °C | 5 | 45 | 1 | 30 |
| `coolingEfficiency` | Cooling COP | ratio | 1.5 | 6 | 0.1 | 3.5 |

### agents

Time unit: min. Evaluation horizon: 30. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L195-L201).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `arrivalRate` | Incoming tasks | tasks/min | 2 | 40 | 1 | 12 |
| `agentCount` | Active agents | agents | 1 | 12 | 1 | 4 |
| `serviceRate` | Per-agent capacity | tasks/min | 1 | 10 | 0.5 | 4 |
| `coordinationPct` | Coordination overhead | % | 0 | 70 | 5 | 20 |

### markets

Time unit: h. Evaluation horizon: 24. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L202-L208).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `baseSpreadBps` | Base spread | bps | 0 | 100 | 1 | 35 |
| `feeBps` | Round-trip fees | bps | 0 | 50 | 1 | 15 |
| `slippageBps` | Slippage estimate | bps | 0 | 30 | 1 | 8 |
| `notionalUSD` | Scenario notional | USD | 1000 | 100000 | 1000 | 10000 |

### control

Time unit: s. Evaluation horizon: 20. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L209-L215).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `setpoint` | Step target | units | 10 | 100 | 5 | 60 |
| `damping` | Damping ratio | ζ | 0.1 | 2 | 0.05 | 0.5 |
| `naturalFrequency` | Natural frequency | rad/s | 0.2 | 3 | 0.1 | 1 |
| `gain` | Steady-state gain | × | 0.5 | 1.5 | 0.05 | 1 |

### security

Time unit: min. Evaluation horizon: 60. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L216-L222).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `alertRate` | Incoming alerts | alerts/min | 2 | 60 | 1 | 20 |
| `analystCount` | Analysts | people | 1 | 12 | 1 | 4 |
| `reviewRate` | Review capacity | alerts/min/person | 1 | 10 | 0.5 | 4 |
| `automationPct` | Automatic resolution | % | 0 | 90 | 5 | 35 |

### charging

Time unit: min. Evaluation horizon: 120. Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L223-L229).

| Key | Label | Declared unit | Minimum | Maximum | UI step | Engine default |
|---|---|---|---:|---:|---:|---:|
| `capacityKWh` | Battery capacity | kWh | 20 | 120 | 5 | 60 |
| `chargerKW` | Charger power | kW | 5 | 180 | 5 | 60 |
| `initialSoc` | Initial charge | % | 5 | 70 | 5 | 20 |
| `efficiencyPct` | Charge efficiency | % | 75 | 99 | 1 | 92 |

## Symbol reuse and implicit constants

These conflicts are retained as local definitions, not silently standardized:

- $Q$ means capacity in the battery/charging explanations, while the thermal display equation uses Q for heat input. This handbook uses $q$ for thermal input and $C_T$ for thermal capacity to disambiguate its prose; the code and display are unchanged.
- $R$ means resistance in the discharge model, a completion rate in the agent queue, and a processed count in the active workload explanation. Always include the code metric and unit when combining results.
- $t$ means hours, minutes, seconds, or cycles depending on the branch. `evaluateModel` does not convert a caller's intended unit; the caller must use the declared `timeUnit`.
- The `reviewedAlerts` key remains unchanged although the active lesson label says “Processed findings.” Neither name implies accepted engineering evidence.
- The control model's `setpoint` and `output` use generic “units.” No physical plant or sensor scale is identified.
- Discharge voltage/thermal coefficients, aging coefficients, synthetic workload waves, cooling inlet coefficients, and dispatch shapes are literal teaching constants. A dimensional interpretation can explain their algebra, but it must not be presented as a measured source.

Source declarations and dispatch: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L159-L319). Selected relabeling: [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L100-L144).

## Tolerances and precision

JavaScript uses its standard finite-number arithmetic for these models. The active lesson's eight checkpoints declare an absolute tolerance of 0.02; the UI's display-decimal choices are formatting, not uncertainty estimates. A percentage checkpoint tolerance of 0.02 means 0.02 percentage points, while a backlog tolerance of 0.02 means 0.02 findings. Native date comparisons use calendar-day integers; native text and identifier rules do not inherit the browser's tolerance. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L146-L305) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L320-L334)

No numerical integration accuracy, measurement precision, confidence interval, or validated uncertainty budget is declared for the active workload model. The [verification ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md) separates arithmetic checks from claims that require external measurements.
