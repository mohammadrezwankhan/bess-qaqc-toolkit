# Failure modes and technical debt

[Handbook](../INDEX.md) · [Troubleshooting](../developer/TROUBLESHOOTING.md) · [Roadmap](../../ROADMAP.md)

These source-backed limitations apply to `af44c932684dfd120dea05d150cefcc3e47539a0`. Proposed remedies are not implemented by the documentation package.

| ID | Failure mode and consequence | Current control / proposed next decision |
|---|---|---|
| BESS-F01 | Readiness coverage derives from recognized records; an unrecognized selected file can disappear | Maintain an input manifest; specify a selected-source contract and negative fixture |
| BESS-F02 | Handover approval dates require content but not calendar syntax | Review dates independently; propose explicit date validation |
| BESS-F03 | Handover does not invoke the punch auditor's independent-verifier rule | Run both relevant auditors; specify composition without weakening either |
| BESS-F04 | Pipe-table scan can see table-like content in fences/comments | Keep record input separate; define accepted grammar before a parser change |
| BESS-F05 | Some template vocabulary exceeds the example status policy | Establish a compatibility matrix; do not silently broaden allowlists |
| BESS-F06 | Lychee excludes the new handbook and several root docs | Run local handbook checks; propose scoped CI coverage |
| BESS-F07 | Browser capacity percentages can be confused with evidence acceptance | Retain synthetic labels; require empirical provenance for operational claims |
| BESS-F08 | JSON outputs lack a declared versioned compatibility contract | Document fixtures and evolution policy before external automation relies on fields |
| BESS-F09 | Nine generic browser model branches are exported but not selected | Document units/assumptions and avoid native validated-BESS claims |
| BESS-F10 | Source, history, CI, and deployed artifacts can refer to different revisions | Preserve each identity and explicit mappings |

## Evidence by finding

- **F01:** [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L78-L113) and [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240). A mixed recognized/unrecognized input diagnostic reproduced the limit.
- **F02 / F03:** [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621) versus [scripts/audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_punch_list.py#L174-L184). Mutated handover fixtures reproduced the narrower checks.
- **F04:** [scripts/validate_templates.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/validate_templates.py#L64-L90) versus separate [scripts/validate_templates.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/validate_templates.py#L106-L125).
- **F05:** [templates/supplier-document-review-tracker.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/templates/supplier-document-review-tracker.md#L1-L36) versus [config/readiness-status-policy.example.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/config/readiness-status-policy.example.json#L1-L36). Template Review Status terms exceed the example allowlist; blank templates can still pass conditional completeness.
- **F06:** [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L98-L104).
- **F07 / F09:** [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L129-L144) and [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L159-L335).
- **F08:** Direct JSON emission in [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506) has no declared report-version contract.
- **F10:** [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L15-L46), [docs/native-lessons.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/native-lessons.json#L1-L30), and [AUDIT_REPORT.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AUDIT_REPORT.md#L1-L24).

## Operational mistakes to diagnose first

**Wrong input selection.** Confirm cwd, explicit paths, immediate-directory expansion, recognized headers, and generated-report markers. Directory arguments are not recursive. Preserve the input manifest. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L137-L163) [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L85-L125)

**Wrong policy semantics.** A per-column rule replaces the fallback; supplied repeatable status options replace default sets in the relevant CLI. Inspect the invocation before changing a policy. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L279-L312) [scripts/audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_evidence_traceability.py#L501-L514)

**Wrong date.** Fixture dates are part of reproducibility. For real records, record the actual assessment date instead of changing it to obtain a pass. Calibration's `--as-of` is optional; several other audit commands require it.

**Report clobbering.** Input-selection boundaries do not sandbox output paths. The command creates parents and writes the requested report location. Use a separate report area. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506)

**One gate mistaken for the full assurance process.** Readiness does not subsume evidence, calibration, punch, handover, or document-control auditors. The appropriate project workflow may require several checks plus independent engineering review.

## Remediation boundaries

A later implementation change should define behavior, reproduce the demonstrated defect with a narrowly scoped fixture, preserve existing gates, pass the regression suite, and update evidence. Do not resolve a limitation by weakening acceptance criteria or relabeling unrecognized inputs as verified.

[AUDIT_REPORT.md](../../AUDIT_REPORT.md), [REMEDIATION_REPORT.md](../../REMEDIATION_REPORT.md), [TEST_VERIFICATION_REPORT.md](../../TEST_VERIFICATION_REPORT.md), and [SAFETY_AND_RESIDUAL_RISK.md](../../SAFETY_AND_RESIDUAL_RISK.md) remain dated evidence. This chapter adds current command-specific qualifications without rewriting historical observations or implying prior authors approved the new proposals.
