# Architecture decision record index

[Handbook](../../INDEX.md) · [Governance](../GOVERNANCE_AND_SCOPE.md) · [Architecture](../../developer/ARCHITECTURE.md)

## Status and evidence

No earlier formal ADR directory was present in the analyzed tree at `af44c932684dfd120dea05d150cefcc3e47539a0`. The entries below distinguish **reconstructed observations** from **proposed decisions**. An observed design is not evidence of who approved it, when they approved it, or which alternatives they considered.

| ID | Subject | Status |
|---|---|---|
| ADR-OBS-001 | Markdown records with explicit Python policy checks | Reconstructed architectural observation |
| ADR-OBS-002 | Specialized auditors remain distinct from readiness | Reconstructed architectural observation |
| ADR-OBS-003 | Static synthetic lesson and native record tools | Reconstructed architectural observation |
| ADR-OBS-004 | Source-pinned historical provenance | Reconstructed architectural observation |
| ADR-PROP-001 | Explicit selected-source and composed-gate contracts | Proposed; owner decision required |

## ADR-OBS-001 — Markdown and policy-driven records

**Observation.** Templates and examples are Markdown tables, parsed by standard-library Python scripts. JSON policies select controlled vocabulary and conditional required fields. Commands can produce Markdown or JSON reports. [scripts/validate_templates.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/validate_templates.py#L64-L90) [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L207-L276) [scripts/audit_completeness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_completeness.py#L89-L201)

**Consequences inferred from the implementation.** Reviewers can inspect and version record text without a service deployment. The accepted table grammar, headers, path selection, and policy semantics are part of the actual interface. The parser is smaller than a complete Markdown renderer, so authoring arbitrary Markdown does not guarantee an intended record will be recognized.

**Unknown historical rationale.** No contemporaneous decision record establishes why this format was chosen or what alternatives were evaluated. Keep this entry as a reconstruction.

## ADR-OBS-002 — Distinct audit gates

**Observation.** Readiness composes status, deadline, and completeness checks. Evidence, calibration, punch-list, handover, and document-control checks are separate commands and separate CI steps. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240) [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L57-L96)

**Consequences.** A clean readiness report does not certify every specialized gate. Handover does not inherit the punch auditor's critical-verifier predicate. The project workflow must select and preserve the applicable command outputs.

**Unknown historical rationale.** The code supports this separation, but an original approval record for the architecture was not identified. This handbook documents the behavior without asserting past intent.

## ADR-OBS-003 — Static teaching layer

**Observation.** A static browser lesson selects the shared `security` model and relabels it as fictional evidence-review workload. The page embeds its own JavaScript arithmetic. It does not call native Python record auditors. GitHub Actions uploads `docs` to Pages. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L54-L144) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L305-L308) [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82)

**Consequences.** The lesson can illustrate demand/capacity relationships without project data. A browser checkpoint is not a native audit or engineering approval. The other nine exported teaching branches must not be presented as a validated BESS plant model.

**Provenance limit.** The present implementation establishes the separation; it does not establish a historical design vote or promise browser-version support.

## ADR-OBS-004 — Historical source pins

**Observation.** The lesson and portfolio materials contain explicit source revisions and source-path references that can predate the current source snapshot. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L15-L46) [docs/native-lessons.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/native-lessons.json#L1-L30) [scripts/portfolio/validate_guide.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/portfolio/validate_guide.py#L1-L33)

**Consequences.** A source-linked lesson is reproducible only when its own pin remains visible. Updating a handbook does not justify replacing historical pins automatically. Deployment provenance must separately identify the served artifact.

## ADR-PROP-001 — Explicit input and gate contracts

**Problem.** Optional readiness coverage is based on recognized records, and handover's predicates differ from the dedicated punch-list auditor. These boundaries can be misread as broader assurance. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L78-L113) [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621)

**Proposal.** Define a selected-input manifest contract and an explicit composition contract for project workflows. Decide whether handover should reuse stricter predicates or require the separate outputs as an enforced workflow step. Preserve current blocking rules and make compatibility changes explicit.

**Alternatives to assess.** Keep separate commands with a documented manifest; introduce a narrowly scoped composition layer; or share selected validation helpers. Evaluate duplicated rules, JSON compatibility, failure visibility, and test coverage.

**Acceptance evidence.** Reproduce the known gaps with negative fixtures, obtain owner review of expected behavior, run all existing checks, and update the claim-to-test map. See [BESS-R01, R02 and R10](../../../ROADMAP.md). No proposed application change is implemented by this documentation package.

## Recording future decisions

A future accepted ADR should name the decision owner, date, context, evidence, alternatives, chosen behavior, consequences, compatibility/migration implications, and related verification. Change status only after an actual decision; do not turn a reconstructed observation into a historical approval retrospectively.
