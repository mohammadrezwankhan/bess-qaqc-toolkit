# Assumptions and limits

[Handbook](../INDEX.md) · [Equations](EQUATIONS_AND_DERIVATIONS.md) · [Failure modes](../maintainer/FAILURE_MODES_AND_TECH_DEBT.md)

## Claim boundary

This repository supplies project-neutral Markdown templates, Python record validators, examples, and static teaching pages. A passing software check means that the selected inputs satisfied that check's implemented conditions. It does not demonstrate equipment safety, calibrated instrumentation in the field, authentic evidence, competent review, regulatory conformity, or authorization to energize. This follows both the implemented record-only interfaces and the existing safety report. [SAFETY_AND_RESIDUAL_RISK.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/SAFETY_AND_RESIDUAL_RISK.md#L1-L84) [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L129-L144)

| Evidence available here | Conclusion it can support | Conclusion requiring additional evidence |
|---|---|---|
| Parsed template and record fixture | Structural or rule behavior for that selected input | Every project document was included or correctly authored |
| Accepted evidence metadata | Recorded relationships and acceptance labels are consistent with selected rules | File exists, is unmodified, authentic, complete, or approved by the named person |
| Calibration dates in a register | Recorded measurement date lies in the required accepted interval | Certificate validity, traceability chain, instrument condition, or measurement uncertainty |
| Named independent verifier string | Text satisfies the punch auditor's separate-owner rule | Verifier identity, independence, competence, or actual witnessed result |
| Browser queue checkpoint | Declared synthetic arithmetic meets its configured comparison | A real reviewer team can safely achieve the modeled rate |
| Green historical CI or local test run | The observed revision and environment passed the recorded commands | A later candidate, deployed page, or real installation has the same outcome |

## Input assumptions and parser limits

The table reader is a small Markdown pipe-table parser. It understands escaped pipes and skips fenced code and HTML comments but is not a full CommonMark renderer. Other Markdown structures outside its grammar may still require human inspection. [scripts/validate_templates.py](../../scripts/validate_templates.py)

Directory arguments select immediate `*.md` files; they do not recursively traverse a project archive. Relative paths are checked against the working-directory boundary. An explicit absolute path selects the external location the caller chose, subject to resolution and symlink checks. These controls do not protect an output destination from accidental overwrite; choose a separate report directory. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L137-L163) [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506)

The selection must contain the intended register schema and policy vocabulary. A status column alone is not sufficient evidence that every relevant requirement has been checked. Some templates intentionally contain blank records or broader editorial vocabulary than an example enforcement policy. Review adaptations, including the supplier tracker vocabulary, before using a policy as a project gate. [config/readiness-status-policy.example.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/config/readiness-status-policy.example.json#L1-L36) [templates/supplier-document-review-tracker.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/templates/supplier-document-review-tracker.md#L1-L36)

## Specific implementation limits observed at the source snapshot

### L1 — Historical selected-source coverage omission

At source snapshot `af44c932684dfd120dea05d150cefcc3e47539a0`, coverage rows came only from recognized records. A local diagnostic pairing a passing record with an unrecognized file reproduced an omitted source. The current implementation records each selected non-generated Markdown input and shows uncovered controls; strict coverage fails on its gaps. The historical reproduction does not mean the file was analyzed at that earlier revision. See the current [API contract](../developer/API_CLI_AND_INTERFACES.md) and [roadmap](../../ROADMAP.md). [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L78-L113) [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240)

### L2 — Handover approval dates have presence checks

The handover auditor requires recorded approval fields for applicable decisions but does not parse those approval dates as calendar dates. A nonblank invalid date in an otherwise passing handover fixture produced no handover findings in the local diagnostic. The document-control, deadline, calibration, and punch auditors have their own date handling; their checks are not automatically inherited by handover. Review approval dates independently. [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621)

### L3 — Handover does not apply the punch verifier predicate

The handover auditor requires nonblank closeout notes and evidence for closed items. It does not invoke the punch-list auditor's stricter critical-item verification rule. A closed Critical item with a generic nonblank note in the handover fixture produced no handover finding in the local diagnostic. Run the dedicated punch-list audit and review the record, rather than interpreting a handover result as proof that all punch rules executed. [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621) [scripts/audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_punch_list.py#L174-L184)

These historical observations qualify the earlier source snapshot. Historical audit reports remain preserved as dated reports; broad statements there should be read alongside these current command-specific limits. The current parser changes remain limited to excluding fenced code and HTML comments, and do not claim full Markdown parsing or replace project review.

## Workload model assumptions

The selected browser lesson assumes constant incoming rate, identical reviewer throughput, instantly available capacity, an empty initial queue, and correct automated clerical triage. All counts are fictional. It has no stochastic arrivals, service-time distribution, severity weighting, reviewer fatigue, batching, startup delay, rework, false positives, false negatives, or traceability to project evidence. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L129-L144) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L305-L308)

Initial condition is $B(0)=0$; there is no configurable preexisting backlog. Inputs remain constant within one evaluation. Time is clamped to 0–60 minutes. There are no spatial boundary conditions because this is a scalar workload formula. The model cannot estimate queue-clearing time for an existing backlog: at excess capacity its current equation simply keeps an initially empty backlog at zero.

A constant capacity ratio is useful for explaining how demand can exceed nominal capacity. It is insufficient for staffing commitments or evidence-acceptance decisions without independently obtained and appropriately governed measurements. No empirical fit or field validation is supplied.

## Other teaching-model assumptions

The shared engine includes nine inactive branches. Their explicit assumptions are retained in the source: simplified ohmic discharge, one thermal mass, exponential cycle fade, fixed-power dispatch, heuristic compute cooling, deterministic agent coordination, synthetic price waves, ideal second-order response, and tapered charging. Each omits domain processes that would be necessary for a credible physical or operational prediction. They remain callable interfaces and are documented in the [equation catalog](EQUATIONS_AND_DERIVATIONS.md#3-other-callable-teaching-model-branches); they are not selected native BESS models. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L159-L229)

The engine evaluates closed forms and arithmetic expressions. Plotted samples and animation frames are presentation choices, not evidence of numerical convergence or solver verification. The template toolkit contains no battery dataset or calibration procedure that validates those teaching constants. The repository's visual scope explicitly describes a checklist and commissioning toolkit rather than a simulated plant. [assets/svg-2.5d/scope.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/assets/svg-2.5d/scope.json#L1-L6)

## Provenance and reproducibility

Source permalinks in this handbook pin the analyzed revision. Existing browser and portfolio provenance records contain their own earlier source pins; those are preserved historical provenance, not silently retargeted to the latest revision. A current claim must identify which artifact and revision it describes. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L15-L46) [docs/native-lessons.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/native-lessons.json#L1-L30)

The local verification observation is dated 2026-11-19. The earlier audit/remediation reports contain their own dates and test totals. A newer count does not invalidate their historical observation, and their passing outcomes do not automatically certify the new documentation candidate. See the [verification ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md).

## Unresolved external facts

This documentation does not infer a live deployment's revision from its URL, infer a required branch rule from a workflow file, or infer project acceptance authority from a GitHub account. Repository settings, protected-branch rules, open work, release metadata, and a deployed page require separate current evidence. Owner and maintainer runbooks specify how to establish those facts before release or publication.
