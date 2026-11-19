# Equations and derivations

[Handbook](../INDEX.md) · [Parameters and symbols](PARAMETERS_AND_SYMBOLS.md) · [Assumptions and limits](ASSUMPTIONS_AND_LIMITS.md)

This chapter distinguishes the native record checks from the browser's synthetic teaching models. It describes source revision `af44c932684dfd120dea05d150cefcc3e47539a0`. Algebra marked **derivation** explains the implementation; it does not establish empirical validity.

## 1. Native QA/QC checks: discrete rules

The native toolkit parses Markdown records and evaluates predicates, relationships, dates, and counts. It does not integrate battery electrochemistry, electrical networks, thermal propagation, or plant dynamics. The repository's declared diagram scope also states that no simulated plant is represented. [assets/svg-2.5d/scope.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/assets/svg-2.5d/scope.json#L1-L6)

### Status, deadline, completeness, and readiness

For a selected status column, let $A$ be its configured allowed values, $F$ its blocking values, and $s$ a normalized recorded status. A status finding is produced for a blocked value, an unknown value when an allowlist exists, or a missing value when that column requires one. A column-specific rule replaces the global rule; it is not their union. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L279-L312)

For a parseable due date $d$ and explicit assessment date $a$, define the signed calendar-day difference

$$
\Delta_d=(d-a).\mathrm{days}.
$$

Negative means overdue, zero means due today, and positive means upcoming. Terminal statuses are classified as closed; missing nonterminal dates have a separate missing state. Parsing of a supplied date still occurs before the terminal-state classification, so a terminal label does not make a malformed date valid. The standalone deadline CLI fails only for states selected by `--fail-on`; the composed readiness gate defaults to failing overdue and missing dates. [scripts/audit_deadlines.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_deadlines.py#L78-L180) [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L40-L75)

Conditional completeness is an implication, not a universal nonblank-cell test:

$$
\text{row matches rule }r \quad\Longrightarrow\quad
\text{every required field group in }r\text{ has a nonmissing value}.
$$

Alternative column names within one field group are alternatives. Unmatched rows are skipped; the command also rejects a run in which no completeness rule matched. Project placeholders are controlled by policy. [scripts/audit_completeness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_completeness.py#L216-L326) [scripts/audit_completeness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_completeness.py#L430-L475)

Conceptually, readiness passes when its selected status, deadline, and completeness components have no gate failures, together with the optional coverage condition. This is a Boolean composition, not a numerical readiness score or evidence-weighted percentage. It does not invoke the separate calibration, evidence, punch-list, handover, or document-control auditors. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240)

**Coverage limit:** the optional coverage calculation uses sources that produced recognized records. A supplied file with no recognized tables can be absent from that universe. It therefore does not prove that every file in the input selection contributed a record. Maintain an independent input manifest and run the specialized checks appropriate to the release decision. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L78-L113) [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240)

### Evidence and calibration relationships

Evidence traceability checks identifier uniqueness, reference resolution, required metadata, acceptance status for completed checks, and unreferenced evidence. The relationship is a controlled-record join:

$$
\mathrm{evidenceIDs}(\mathrm{completed\ check})
\subseteq
\mathrm{IDs}(\mathrm{accepted\ evidence\ records}).
$$

This abbreviated predicate is explanatory: the actual auditor has additional format, duplicate, missing-field, and orphan checks. A populated evidence location is metadata; the command does not open the referenced file or authenticate its contents. [scripts/audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_evidence_traceability.py#L208-L393)

Calibration periods are inclusive. For a completed measurement at date $d_m$, a candidate record covers it when

$$
d_{\mathrm{from}}\le d_m\le d_{\mathrm{through}}.
$$

The completed measurement must resolve to exactly one covering accepted calibration record for the referenced instrument. Overlapping periods are rejected; two inclusive intervals that touch on the same date overlap. Planned measurements are not subject to the same completed-measurement coverage requirement. When an `as_of` date is supplied, a completed measurement after that date is also a finding. [scripts/audit_calibration_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_calibration_traceability.py#L236-L553) [scripts/audit_calibration_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_calibration_traceability.py#L556-L572)

### Punch closeout, handover, and revision control

Punch closeout uses categorical rules. Active critical items block; closed critical items require the exact structured independent-verification text accepted by the parser, including a verifier different from the recorded owner. This checks text and roles as recorded, not the identity or competence of an actual person. [scripts/audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_punch_list.py#L174-L184) [scripts/audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_punch_list.py#L187-L338)

Handover performs a separate join between punch IDs, residual-risk records, and an acceptance decision. Its policy defines blocking and nondeferrable classes. The supplied policy treats Critical and Major as blocking while active and Critical as nondeferrable. It does not call the punch-list auditor's independent-verifier predicate. Approval-date fields in this auditor are checked for presence, not parsed as dates. Run both auditors and review the real authorization records. [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621) [config/handover-acceptance-policy.example.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/config/handover-acceptance-policy.example.json#L1-L24)

Document control parses one alphabetic or numeric revision scheme per document, requires chronological issue dates, accepted current revisions, obsolete historical revisions, and an immediate-predecessor supersedes relationship. These revision values are not semantic software versions. [scripts/audit_document_control.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_document_control.py#L149-L157) [scripts/audit_document_control.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_document_control.py#L169-L389)

### Human document-readiness scale

The document readiness template defines an ordinal 0–4 scale: Missing, Draft, Submitted, Approved, Accepted. It suggests a score column for human closeout review. The template does not define averaging, weighting, a numerical acceptance threshold, or a physical safety margin, and the native readiness command does not compute a composite score from it. Do not treat the distance between categories as a measured interval. [Scoring guide](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/templates/document-readiness-scoring-guide.md#L1-L22).

## 2. Active browser lesson: review workload

The selected `security` branch is relabeled in this repository as evidence-review workload. Its four inputs and all lesson presets are fictional. The browser does not parse project records or run the Python acceptance policies. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L54-L144)

Let:

- $\lambda$ be the incoming rate in findings/minute;
- $a$ be the assumed correctly resolved clerical-triage fraction in percent;
- $n$ be reviewer count and $\mu$ be findings/minute/reviewer;
- $t$ be elapsed minutes, with an empty initial queue.

The literal implementation computes manual demand $d$, manual capacity $c$, backlog $B$, nominal coverage $C$, processed findings $R$, and reviewer utilization $U$ as

$$
d=\lambda(1-a/100),\qquad c=n\mu,
$$

$$
B(t)=\max(0,d-c)t,
$$

$$
C=100\min\left(1,\frac{\lambda a/100+c}{\lambda}\right),
$$

$$
R(t)=\left(\lambda a/100+\min(d,c)\right)t,
\qquad
U=100\min(1,d/c).
$$

Source: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L305-L308).

**Derivation.** With constant rates and zero initial backlog, unresolved manual work grows at $d-c$ only when demand exceeds capacity. Integrating that constant positive rate yields $B(t)$. Automatically resolved and manually completed rates add to the processed count. Within this model,

$$
B(t)+R(t)=\lambda t.
$$

This is a useful conservation identity for the fictional count model. It is not evidence that an engineering finding was correctly resolved. Coverage is a capacity ratio capped at 100%, not a fraction of independently verified engineering requirements. It remains a rate ratio even at $t=0$.

### Reproducing the four configured lessons

All eight configured checkpoints evaluate at $t=60$ minutes with absolute tolerance `0.02` in the checkpoint metric's units. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L146-L305)

| Lesson | $(\lambda,n,\mu,a)$ | Manual rate / capacity | Expected values |
|---|---|---|---|
| Separate workload from acceptance | $(12,2,4,0)$ | $12/8$ findings/min | $C=66.666666\ldots\%$, $B=240$ findings |
| Add review capacity | $(12,3,4,0)$ | $12/12$ findings/min | $C=100\%$, $B=0$ |
| Increase incoming work | $(20,3,4,0)$ | $20/12$ findings/min | $C=60\%$, $B=480$ |
| Apply assumed clerical triage | $(20,3,4,40)$ | $12/12$ findings/min | $C=100\%$, $R=1200$ findings |

The fourth scenario assumes that eight findings/minute are correctly triaged and twelve are manually completed. It does not implement an automated engineering approval mechanism.

### Evaluation and comparison semantics

The engine evaluates closed-form formulas directly. There is no differential-equation integrator, mesh, timestep convergence procedure, or stochastic sampling in this branch. Finite input numbers are clamped to parameter bounds; nonnumeric or nonfinite values use engine defaults. Finite time is clamped to the model horizon, and nonfinite time becomes zero. Direct API inputs are not snapped to slider steps. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L235-L246)

Checkpoint equality accepts $|x-x_\mathrm{expected}|\le \varepsilon$. Greater-or-equal and less-or-equal comparisons relax their bounds by $\varepsilon$; strict greater-than/less-than comparisons ignore tolerance. Unknown metrics, nonnumeric expectations, and unsupported operators produce `invalid`. These tolerances belong to teaching checkpoints, not engineering acceptance measurements. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L320-L334)

## 3. Other callable teaching-model branches

Nine additional branches are present in the shared exported engine, although this repository's selected lesson is the workload branch. Their implementation is accounted for here so that their presence is not mistaken for a hidden native BESS simulator. They are simplified, uncalibrated teaching formulas. The symbols below are local to each branch; the same letter is not a portfolio-wide physical definition.

### Battery discharge

For capacity $Q$ in Ah, requested current $I$ in A, elapsed $t$ in hours, resistance $R$ in ohms, ambient $T_a$, and initial percentage $S_0$:

$$
S=\operatorname{clamp}(S_0-100It/Q,0,100),\quad
I_e=\begin{cases}I&S>0\\0&S=0,\end{cases}
$$

$$
V=320+0.8S-I_eR,\quad P=VI_e/1000.
$$

Depletion time is $t_e=QS_0/(100I)$ for $I>0$ and infinity for $I=0$. With $t_h=\min(t,t_e)$ and $t_c=\max(0,t-t_e)$,

$$
T=T_a+\frac{I^2R}{8}(1-e^{-t_h/0.8})e^{-t_c/0.8}.
$$

The numerical coefficients and 0.8-hour relaxation are illustrative implementation constants. The voltage law is linear in SOC; current becomes zero at depletion. No calibration, BMS, pack topology, aging, or protection behavior is represented. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L160-L166) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L248-L256)

### Single thermal mass

Let heat input be $q$ W, conductance $h$ W/K, heat capacity $C_T$ J/K, and displayed time $t$ minutes:

$$
\Delta T=(q/h)(1-e^{-h(60t)/C_T}),\quad T=T_a+\Delta T,
$$

$$
q_\mathrm{removed}=h\Delta T,\quad E=C_T\Delta T/1000,\quad
q_\mathrm{net}=q-h\Delta T.
$$

**Derivation:** this is the closed-form solution of $C_T\,d\Delta T/d\tau=q-h\Delta T$ with $\Delta T(0)=0$ and $\tau=60t$ seconds. The one-node model omits spatial gradients and phase change. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L167-L173) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L257-L260)

### Cycle aging proxy

For coefficient $f$ labeled percent/1000 cycles, constant temperature $T$, C-rate $r$, initial capacity $Q_0$, and continuous cycle coordinate $t$:

$$
k=(f/100000)e^{(T-25)/20}\sqrt r,\quad x=e^{-kt},
$$

$$
\mathrm{retention}=100x,\quad Q=Q_0x,\quad
\mathrm{resistanceGrowth}=200(1-x),
$$

$$
E_\mathrm{throughput}=\frac{3.7Q_0}{1000}\frac{1-e^{-kt}}{k}.
$$

The final expression is the integral of the declining capacity proxy times an illustrative 3.7 V. The code uses `-Math.expm1(-k*t)` for its numerator. These coefficients are not fitted battery-life parameters; calendar aging is omitted. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L174-L180) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L261-L265)

### Daily dispatch proxy

With displayed $t$ in hours, baseline demand $D$, solar amplitude $S_p$, fixed battery contribution $P_b$, and grid-carbon factor $g$:

$$
P_s=S_p\max(0,\sin(\pi(t-6)/12)),
$$

$$
P_d=D\left(0.8+0.18\cos(2\pi(t-19)/24)+0.12e^{-((t-19)/3)^2}\right),
$$

$$
P_g=\max(P_d-P_s-P_b,0),\quad
\mathrm{solarShare}=100\min(1,P_s/P_d),\quad
\mathrm{emissions}=P_g g/1000.
$$

Powers are kW and emissions are kg/hour. Battery energy inventory and charging are absent. The share metric counts solar, not the fixed battery contribution, and exported power is not credited. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L181-L187) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L266-L271)

### Compute cooling proxy

For server count $N$, nominal utilization $U_0$ percent, COP $\eta$, ambient $T_a$, and minutes $t$:

$$
u=\operatorname{clamp}(U_0+8\sin(t/8)+3\cos(t/3),0,100),
$$

$$
P_\mathrm{IT}=N(0.12+0.38u/100),\quad
P_c=\frac{P_\mathrm{IT}}{\eta}(1+0.025\max(T_a-20,0)),\quad
\mathrm{PUE}=1+P_c/P_\mathrm{IT},
$$

$$
T_\mathrm{in}=22+(T_a-22)e^{-t/15}
+\frac{4P_\mathrm{IT}}{N\eta}(1-e^{-t/15}).
$$

Powers are kW. The inlet expression is a heuristic evaluated using the instantaneous synthetic IT load; it is not a solved coupled airflow/thermal state equation. Coefficients have implicit units in the formula and are not sourced equipment characteristics. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L188-L194) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L272-L278)

### Agent coordination queue

For arrival rate $\lambda$, agent count $n$, per-agent rate $\mu$, and overhead $o$ percent:

$$
c=n\mu\left(1-\frac{o}{100}\frac{n-1}{n}\right),\quad
B=\max(0,\lambda-c)t,\quad R=\min(\lambda,c),
$$

$$
U=100\min(1,\lambda/c),\quad W=B/c+1/\mu.
$$

Here $R$ is a completion **rate**, unlike the accumulated processed-count metric of the active workload branch. $W$ is a deterministic proxy for delay, not a stochastic queueing theorem or measured service-level guarantee. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L195-L201) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L279-L283)

### Price-spread scenario

With basis-point inputs $b$, fees $f$, slippage $s$, notional $N$ USD, and hours $t$:

$$
b_t=b+12\sin(2\pi t/12)+5\sin(2\pi t/5),\quad e=b_t-f-s,
$$

$$
\mathrm{PnL}=Ne/10000,\quad \mathrm{cost}=N(f+s)/10000.
$$

This is one hypothetical opportunity at time $t$, not an integrated return series or a trading interface. All waves and inputs are synthetic. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L202-L208) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L284-L288)

### Second-order response

The documented differential equation is

$$
y''+2\zeta\omega_n y'+\omega_n^2y=K\omega_n^2r,\qquad
y(0)=y'(0)=0.
$$

The implementation evaluates the corresponding normalized step $s(t)$ analytically, with $y=Kr\,s$ and velocity $Kr\,s'$. Let $\omega=\omega_n$.

- For $|\zeta-1|<10^{-8}$: $s=1-e^{-\omega t}(1+\omega t)$ and $s'=\omega^2t e^{-\omega t}$.
- For $\zeta<1$, let $q=\sqrt{1-\zeta^2}$: $s=1-e^{-\zeta\omega t}[\cos(\omega qt)+(\zeta/q)\sin(\omega qt)]$ and $s'=(\omega/q)e^{-\zeta\omega t}\sin(\omega qt)$.
- For $\zeta>1$, let $q=\sqrt{\zeta^2-1}$, $r_1=-\omega(\zeta-q)$, $r_2=-\omega(\zeta+q)$: $s=1+[r_2e^{r_1t}-r_1e^{r_2t}]/(r_1-r_2)$ and $s'=r_1r_2[e^{r_1t}-e^{r_2t}]/(r_1-r_2)$.

The error metric is $r-y$, while theoretical overshoot is relative to the final $Kr$ level: $100e^{-\zeta\pi/\sqrt{1-\zeta^2}}$ for $\zeta<1$, otherwise zero. Thus nonunit gain changes steady error without changing the definition of theoretical overshoot. There is no discrete controller, saturation, sensor model, or numerical ODE solver. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L209-L215) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L289-L304)

### Charging proxy

For capacity $Q$ kWh, charger power $P_\mathrm{in}$ kW, efficiency $\eta$ percent, initial percentage $S_0<80$, and $h=t/60$ hours:

$$
P_e=P_\mathrm{in}\eta/100,\quad
h_{80}=(80-S_0)Q/(100P_e),\quad
\tau=0.2Q/P_e.
$$

Before taper, $S=S_0+100P_eh/Q$ and $P=P_e$. After taper begins,

$$
S=100-20e^{-(h-h_{80})/\tau},\quad
P=P_e e^{-(h-h_{80})/\tau}.
$$

Stored energy is $(S-S_0)Q/100$ and loss power is $P(100/\eta-1)$. SOC and charge power are continuous at 80%; the exponential approaches 100% asymptotically. The model does not implement a charger protocol, electrochemical charge limit, temperature constraint, or field-validated charging curve. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L223-L229) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L309-L316)

## 4. Interpretation boundaries

The formulas above are a traceable description of code, not a certification or empirical validation. The active lesson's checkpoints compare arithmetic to declared expectations; native audit tests compare program behavior to controlled fixtures. Neither establishes the correctness of a real project record, reviewer approval, battery design, energization procedure, or regulatory conclusion. See [assumptions and limits](ASSUMPTIONS_AND_LIMITS.md) for the claim-to-evidence boundary and [verification ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md) for what was actually run.
