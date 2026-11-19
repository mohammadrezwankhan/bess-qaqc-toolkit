# Development roadmap

[Handbook](docs/INDEX.md) · [Current findings](docs/maintainer/FAILURE_MODES_AND_TECH_DEBT.md) · [Owner decisions](docs/owner/GOVERNANCE_AND_SCOPE.md)

**Planning window: 2026-11-19 through 2027-11-18.** These are evidence-based proposals, not release commitments, assigned staffing, or features implemented by the documentation update. “Now” covers the remaining 2026 quarter; the next-quarter, later and one-year windows stay within the stated horizon.

The starting source is `af44c932684dfd120dea05d150cefcc3e47539a0`: 35 templates, ten core Python CLIs, 180 locally observed unit tests, separate specialized audit commands, and a synthetic static teaching lesson. Current software checks do not constitute project field validation. See the [verification ledger](docs/maintainer/VERIFICATION_EVIDENCE_LEDGER.md).

The 2026-11-19 repository metadata observation returned no open issues or pull requests and no tags or releases. The items below come from source review and reproducible limitations, not invented issue numbers. New issues/PRs and owner priorities may change the plan.

## Priority and capacity

P1 items reduce ambiguity in what inputs and gates were actually checked or keep documentation verifiable. P2 items strengthen compatibility, reproducibility and recovery after those contracts are settled. Effort ranges are rough focused-work estimates, exclude owner waiting time and field data acquisition, and require replanning when responsibility and capacity are assigned.

| ID | Proposal | Window | Priority | Dependencies |
|---|---|---|---|---|
| BESS-R01 | Make selected-source coverage explicit | Now: 2026-11-19–2026-12-31 | P1 | None |
| BESS-R02 | Resolve handover date and critical-closeout gaps | Next quarter: 2027-01-01–2027-03-31 | P1 | BESS-R01 |
| BESS-R03 | Cover the handbook in documentation CI | Now: 2026-11-19–2026-12-31 | P1 | None |
| BESS-R04 | Map template and policy vocabulary deliberately | Next quarter: 2027-01-01–2027-03-31 | P1 | None |
| BESS-R05 | Define a versioned machine-readable report contract | Later: 2027-04-01–2027-06-30 | P2 | BESS-R01, BESS-R02 |
| BESS-R06 | Specify and test the accepted record-table grammar | Later: 2027-04-01–2027-06-30 | P2 | BESS-R04 |
| BESS-R07 | Evaluate workload-model validity using governed evidence | Within one year: 2027-07-01–2027-09-30 | P2 | BESS-R04 |
| BESS-R08 | Exercise deputy recovery and deployment provenance | Within one year: 2027-07-01–2027-11-18 | P2 | BESS-R03 |
| BESS-R09 | Keep teaching controls and exported engine reproducible | Next quarter: 2027-01-01–2027-03-31 | P2 | BESS-R03 |
| BESS-R10 | Define an explicit project audit composition recipe | Within one year: 2027-07-01–2027-11-18 | P2 | BESS-R01, BESS-R02, BESS-R04, BESS-R05 |

## BESS-R01 — Make selected-source coverage explicit

**Status:** proposed. **Window:** Now: 2026-11-19–2026-12-31. **Suggested owner:** Toolkit maintainer with project assurance reviewer.

**Effort:** 2–4 focused engineering days. **Confidence:** High on reproduced gap; medium on compatibility effort.

**Evidence:** [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L78-L240). Findings: BESS-F01.

**Dependencies:** No planned item prerequisite.

**Risk / assumption:** Rejecting previously ignored files may change callers' outcomes. Decide whether explicit exclusion is permitted and how it is reported.

**Acceptance criteria:**

- A mixed valid/unrecognized selected-file fixture fails or reports an explicit reviewed exclusion; the file never silently disappears.
- Every supplied file has a manifest disposition, and the output names the selected policy and assessment date.
- All existing native checks pass without weakening the current gate.

**Verification:** Negative fixture, existing readiness tests, complete native suite, documented before/after JSON contract.

## BESS-R02 — Resolve handover date and critical-closeout gaps

**Status:** proposed. **Window:** Next quarter: 2027-01-01–2027-03-31. **Suggested owner:** Toolkit maintainer and independent project assurance reviewer.

**Effort:** 3–6 focused engineering days. **Confidence:** High on reproduced gaps; medium on chosen composition.

**Evidence:** [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621), [scripts/audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_punch_list.py#L174-L184). Findings: BESS-F02, BESS-F03.

**Dependencies:** BESS-R01.

**Risk / assumption:** A shared helper or composition layer must preserve stricter punch rules and make optional date fields explicit.

**Acceptance criteria:**

- Owner-approved behavior defines valid approval dates and closed-Critical independent verification across the workflow.
- Invalid nonblank approval dates and generic closed-Critical notes are rejected by the required composed gate.
- Existing accepted deferrals and passing fixtures retain intended behavior; unsupported legacy data has a documented migration path.

**Verification:** Both demonstrated negative cases, boundary/date cases, punch and handover suites, full regression commands.

## BESS-R03 — Cover the handbook in documentation CI

**Status:** proposed. **Window:** Now: 2026-11-19–2026-12-31. **Suggested owner:** Documentation maintainer and repository integration owner.

**Effort:** 1–2 focused engineering days. **Confidence:** High.

**Evidence:** [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L98-L104), [AGENTS.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AGENTS.md#L1-L3). Findings: BESS-F06.

**Dependencies:** No planned item prerequisite.

**Risk / assumption:** Network link checks can be nondeterministic; preserve local/remote distinctions and all existing job contexts, pins and gates.

**Acceptance criteria:**

- All requested root documents and docs/**/*.md are included in local target/anchor and CFF validation as appropriate.
- A deliberately broken handbook target is detected in a controlled CI verification.
- Existing checks and publication routes remain intact; required check behavior is observed against the candidate.

**Verification:** Reviewed workflow diff, controlled broken-link test outside the shipped candidate, exact-revision CI run, restored passing candidate.

## BESS-R04 — Map template and policy vocabulary deliberately

**Status:** proposed. **Window:** Next quarter: 2027-01-01–2027-03-31. **Suggested owner:** Project assurance reviewer and documentation maintainer.

**Effort:** 2–4 focused review days. **Confidence:** High on observed mismatch; medium on project-specific vocabulary.

**Evidence:** [templates/supplier-document-review-tracker.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/templates/supplier-document-review-tracker.md#L1-L36), [config/readiness-status-policy.example.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/config/readiness-status-policy.example.json#L1-L36). Findings: BESS-F05.

**Dependencies:** No planned item prerequisite.

**Risk / assumption:** A universal allowlist could weaken project controls. Distinguish editorial legends from enforceable project policy.

**Acceptance criteria:**

- All 35 templates have documented relevant headers/status vocabularies and their example-policy compatibility.
- Every mismatched term is intentional and explained or has an approved policy/template proposal.
- Representative adapted records demonstrate both accepted vocabulary and rejected typos without widening blocking rules silently.

**Verification:** Template/policy matrix, reviewed fixtures, strict template and policy checks.

## BESS-R05 — Define a versioned machine-readable report contract

**Status:** proposed. **Window:** Later: 2027-04-01–2027-06-30. **Suggested owner:** Toolkit maintainer and intended report consumer.

**Effort:** 4–8 focused engineering days. **Confidence:** Medium; consumer requirements unconfirmed.

**Evidence:** [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506), [scripts/audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_evidence_traceability.py#L542-L612). Findings: BESS-F08.

**Dependencies:** BESS-R01, BESS-R02.

**Risk / assumption:** External consumers and compatibility commitments are not yet established. Avoid declaring stability before their needs are known.

**Acceptance criteria:**

- Documented schemas identify report version, source selection, policy identity, assessment date, selected gates and limitations.
- Golden synthetic fixtures cover pass, findings and input-error cases for the intended consumer surface.
- Compatibility and migration policy is approved before a portfolio consumer depends on it.

**Verification:** Schema validation, fixture round trips, documented compatibility cases, full existing regression suite.

## BESS-R06 — Specify and test the accepted record-table grammar

**Status:** proposed. **Window:** Later: 2027-04-01–2027-06-30. **Suggested owner:** Toolkit maintainer.

**Effort:** 3–5 focused engineering days. **Confidence:** Medium.

**Evidence:** [scripts/validate_templates.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/validate_templates.py#L26-L125). Findings: BESS-F04.

**Dependencies:** BESS-R04.

**Risk / assumption:** Switching parser behavior may alter recognition of existing records; do not add a general Markdown dependency without need and review.

**Acceptance criteria:**

- A documented grammar covers pipes, escaping, empty cells, fences, comments and malformed tables.
- Positive and negative fixtures distinguish instructional table text from intended records.
- All existing templates/examples retain intended recognized content or have explicit reviewed migration notes.

**Verification:** Parser fixtures, record-count comparisons, all native audits and template checks.

## BESS-R07 — Evaluate workload-model validity using governed evidence

**Status:** proposed. **Window:** Within one year: 2027-07-01–2027-09-30. **Suggested owner:** Owner-designated research reviewer.

**Effort:** 3–6 review days after authorized data availability. **Confidence:** Low on data availability; high on current synthetic status.

**Evidence:** [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L54-L144), [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L305-L308). Findings: BESS-F07.

**Dependencies:** BESS-R04.

**Risk / assumption:** Real project records may be confidential or unsuitable. No data collection, disclosure, or empirical staffing claim is authorized by this proposal.

**Acceptance criteria:**

- Owner decides whether a suitable approved deidentified dataset and review question exist; otherwise record a reasoned no-data outcome.
- If data is approved, compare constant-rate assumptions, backlog and throughput errors with stated uncertainty and limits.
- Retain synthetic teaching labels unless a separate reviewed validation supports a narrowly stated empirical claim; never infer engineering acceptance from queue clearance.

**Verification:** Approved data provenance/rights record, reproducible analysis, independent review; no-data outcome is explicit rather than fabricated validation.

## BESS-R08 — Exercise deputy recovery and deployment provenance

**Status:** proposed. **Window:** Within one year: 2027-07-01–2027-11-18. **Suggested owner:** Repository owner and authorized recovery deputy.

**Effort:** 1–3 exercise days after access assignment. **Confidence:** Medium; deputy unassigned in source.

**Evidence:** [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82), [CITATION.cff](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/CITATION.cff#L1-L16). Findings: BESS-F10.

**Dependencies:** BESS-R03.

**Risk / assumption:** Access and signing recovery require owner action. Preserve protections and avoid publishing credentials or confidential recovery details.

**Acceptance criteria:**

- An authorized deputy is explicitly assigned and can restore the pinned source and run native checks.
- A reviewed signed documentation change is traced through required checks, merge and Pages content.
- Sensitive reporting and recovery-channel gaps have named owner decisions and retained evidence.

**Verification:** Dated rehearsal receipt, exact source/check/deployment identities, owner confirmation, sanitized findings.

## BESS-R09 — Keep teaching controls and exported engine reproducible

**Status:** proposed. **Window:** Next quarter: 2027-01-01–2027-03-31. **Suggested owner:** Teaching documentation maintainer.

**Effort:** 2–4 focused engineering days. **Confidence:** High on arithmetic; medium on browser coverage.

**Evidence:** [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L159-L335), [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L146-L305). Findings: BESS-F07, BESS-F09.

**Dependencies:** BESS-R03.

**Risk / assumption:** Generic engine defaults differ from lesson defaults; a seemingly cosmetic change can alter arithmetic or units.

**Acceptance criteria:**

- All eight active lesson checkpoints pass against the declared presets/tolerances.
- Configured versus engine defaults, time units, clamping and invalid comparison behavior are tested and documented.
- Keyboard and narrow-screen checks of the existing lesson are observed separately from arithmetic tests; no physical-validation claim is added.

**Verification:** Sandboxed model/checkpoint assertions plus recorded browser interaction/accessibility review on the actual candidate.

## BESS-R10 — Define an explicit project audit composition recipe

**Status:** proposed. **Window:** Within one year: 2027-07-01–2027-11-18. **Suggested owner:** Project assurance owner and toolkit maintainer.

**Effort:** 3–6 focused design/engineering days. **Confidence:** Medium.

**Evidence:** [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240), [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L57-L96). Findings: BESS-F01, BESS-F03, BESS-F08.

**Dependencies:** BESS-R01, BESS-R02, BESS-R04, BESS-R05.

**Risk / assumption:** Different project phases require different gates; a single green aggregate must not hide unrun checks or substitute for authorization.

**Acceptance criteria:**

- Approved recipes name required commands, source selection, policy revisions, assessment dates and unrun/not-applicable outcomes.
- Synthetic end-to-end records demonstrate failure propagation from each selected specialized gate.
- Reports keep software checks separate from actual human project acceptance; compatibility and recovery instructions are updated.

**Verification:** Reviewed composition specification, representative failing/passing fixtures, report-schema checks and complete existing native suite.

## Review and closure

At each window boundary, review actual owner capacity, new issues, source changes and evidence. Reprioritize openly; do not move unfinished items into “done” because the target date passed. Completion requires the stated acceptance evidence and a real reviewed change or decision.

Application proposals in this roadmap are deliberately separate from the documentation package. Any later implementation must preserve existing validation gates, citation history, signed-commit policy, test evidence and project authorization boundaries. No staffing efficiency, CI cost reduction, field performance or safety improvement is claimed in advance.
