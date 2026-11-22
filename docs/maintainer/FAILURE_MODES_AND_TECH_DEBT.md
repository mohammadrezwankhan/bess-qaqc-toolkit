# Failure modes and technical debt

[Handbook](../INDEX.md) · [Troubleshooting](../developer/TROUBLESHOOTING.md) · [Roadmap](../../ROADMAP.md)

The original findings below were assessed at `af44c932684dfd120dea05d150cefcc3e47539a0`. Historical references retain that evidence revision; the final column records current implementation status for the selected work in issue #101.

| ID | Failure mode observed at the assessed revision | Current implementation status |
|---|---|---|
| BESS-F01 | Readiness coverage derives from recognized records; an unrecognized selected file can disappear | Fixed: every selected non-generated file is represented in the matrix; strict mode fails for missing source/control pairs. Generated reports are listed as explicit exclusions. |
| BESS-F02 | Handover approval dates require content but not calendar syntax | Open: review dates independently; propose explicit date validation. |
| BESS-F03 | Handover does not invoke the punch auditor's independent-verifier rule | Open: run both relevant auditors; specify composition without weakening either. |
| BESS-F04 | Pipe-table scan can see table-like content in fences/comments | Fixed for fenced code and HTML comments; the parser remains a small pipe-table reader, not a complete CommonMark implementation. |
| BESS-F05 | Some template vocabulary exceeds the example status policy | Fixed for included template table values and the supplier review-value list; configured blocking states are unchanged. |
| BESS-F06 | Lychee excludes the new handbook and several root docs | Partial: an offline relative-link check covers selected handbook pages in the existing job; other handbook/root docs and remote handbook URLs remain outside that scope. |
| BESS-F07 | Browser capacity percentages can be confused with evidence acceptance | Open: retain synthetic labels; require empirical provenance for operational claims. |
| BESS-F08 | JSON outputs lack a declared versioned compatibility contract | Partial: combined readiness JSON has schema version 1; standalone audit JSON outputs remain outside this contract. |
| BESS-F09 | Nine generic browser model branches are exported but not selected | Open: document units/assumptions and avoid native validated-BESS claims. |
| BESS-F10 | Source, history, CI, and deployed artifacts can refer to different revisions | Open: preserve each identity and explicit mappings. |

## Evidence by finding

- **F01:** A mixed recognized/unrecognized input diagnostic reproduced the historical limit in [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L78-L113). Current selected-manifest behavior and the negative fixture are in [scripts/audit_readiness.py](../../scripts/audit_readiness.py) and [tests/test_audit_readiness.py](../../tests/test_audit_readiness.py).
- **F02 / F03:** [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621) versus [scripts/audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_punch_list.py#L174-L184). Mutated handover fixtures reproduced the narrower checks.
- **F04:** [scripts/validate_templates.py](../../scripts/validate_templates.py) now filters fenced code and HTML comments before table parsing. Regression fixtures are in [tests/test_validate_templates.py](../../tests/test_validate_templates.py); the original parser locations remain linked in the historical [source snapshot](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/validate_templates.py#L64-L90).
- **F05:** [config/readiness-status-policy.example.json](../../config/readiness-status-policy.example.json) now includes `Planned`, `Pending review`, and all supplier tracker review values. [tests/test_summarize_status.py](../../tests/test_summarize_status.py) checks table values across templates and the supplier review list. The allowed values are not declarations of acceptance or release approval.
- **F06:** [.github/workflows/markdown-maintenance.yml](../../.github/workflows/markdown-maintenance.yml) retains the existing networked root/template check and adds an offline check for selected handbook pages. The exact file scope is documented in the [CI playbook](CI_CD_AND_RELEASE_PLAYBOOK.md).
- **F07 / F09:** [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L129-L144) and [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L159-L335).
- **F08:** [scripts/audit_readiness.py](../../scripts/audit_readiness.py) emits `schema_version: 1`; [config/readiness-report-v1.schema.json](../../config/readiness-report-v1.schema.json) defines the combined readiness shape and compatibility rules. Other standalone audit outputs are not covered.
- **F10:** [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L15-L46), [docs/native-lessons.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/native-lessons.json#L1-L30), and [AUDIT_REPORT.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AUDIT_REPORT.md#L1-L24).

## Operational mistakes to diagnose first

**Wrong input selection.** Confirm cwd, explicit paths, immediate-directory expansion, recognized headers, and generated-report markers. Directory arguments are not recursive. Preserve the input manifest. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L137-L163) [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L85-L125)

**Wrong policy semantics.** A per-column rule replaces the fallback; supplied repeatable status options replace default sets in the relevant CLI. Inspect the invocation before changing a policy. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L279-L312) [scripts/audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_evidence_traceability.py#L501-L514)

**Wrong date.** Fixture dates are part of reproducibility. For real records, record the actual assessment date instead of changing it to obtain a pass. Calibration's `--as-of` is optional; several other audit commands require it.

**Report clobbering.** Input-selection boundaries do not sandbox output paths. The command creates parents and writes the requested report location. Use a separate report area. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506)

**One gate mistaken for the full assurance process.** Readiness does not subsume evidence, calibration, punch, handover, or document-control auditors. The appropriate project workflow may require several checks plus independent engineering review.

## Remediation boundaries

Future follow-up should define behavior, reproduce each defect with a narrowly scoped fixture, preserve existing gates, pass the regression suite, and update evidence. Do not resolve a limitation by weakening acceptance criteria or relabeling unrecognized inputs as verified.

[AUDIT_REPORT.md](../../AUDIT_REPORT.md), [REMEDIATION_REPORT.md](../../REMEDIATION_REPORT.md), [TEST_VERIFICATION_REPORT.md](../../TEST_VERIFICATION_REPORT.md), and [SAFETY_AND_RESIDUAL_RISK.md](../../SAFETY_AND_RESIDUAL_RISK.md) remain dated evidence. This chapter adds current command-specific qualifications without rewriting historical observations or implying prior authors approved the new proposals.
