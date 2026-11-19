# Architecture

[Handbook index](../INDEX.md)

## Purpose and boundaries

The native toolkit reads local Markdown tables and JSON policies, produces Markdown or JSON reports, and returns process exit codes. It has no device-control interface, site telemetry client or automated permission to energize. The browser teaching lab is a separate HTML/JavaScript application. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240) [SAFETY_AND_RESIDUAL_RISK.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/SAFETY_AND_RESIDUAL_RISK.md#L10-L18) [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L139-L144)

## Components and data flow

| Component | Input and responsibility | Output and boundary |
| --- | --- | --- |
| `templates/` | Thirty-five reusable records and guidance files for the delivery lifecycle | Starter content and prompts, including unfinished/example fields; a template is not completed project evidence |
| `validate_templates.py` | H1, introduction, pipe-table structure and optional closeout prompts | Structural findings; no engineering review of a criterion or measurement |
| `summarize_status.py` | File selection, status rows, global or column-specific policy | Status counts and line-located policy violations |
| `audit_deadlines.py` | Recognized status/date columns and explicit audit date | Calendar-day classification |
| `audit_completeness.py` | Conditional JSON rules and matching table rows | Missing-column/value findings |
| `audit_readiness.py` | The three preceding controls and optional per-recognized-source coverage | Combined report; specialized traceability and handover audits are separate commands |
| Specialized audits | Evidence/check registers, calibration history, punch lists, risk/acceptance registers, document history | Their own findings and reports |
| Browser surfaces | Embedded lesson data, sliders and local study notes | Synthetic teaching metrics and exports; no invocation of native audit commands |

The shared parser and policy flows are implemented in [scripts/validate_templates.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/validate_templates.py#L26-L90), [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L85-L163), [scripts/audit_completeness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_completeness.py#L216-L326) and [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240).

The important composition rule is to select every audit needed by the project. `audit_readiness.py` imports status, deadline and completeness code; it does not import the evidence, calibration, punch-list, handover or document-control audits. A clean combined report therefore says nothing about those independent controls. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L11-L65)

## Input selection and parsing

Directory input is a sorted, **nonrecursive** `*.md` scan. Duplicate resolved paths are removed. Relative inputs must remain within the current working directory unless a caller supplies an explicit `base_boundary`; an explicitly absolute input can select an external directory/file. A file symlink escaping its selected directory is rejected. These are input-selection boundaries, not a sandbox for every output path. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L128-L163)

The table parser requires leading/trailing unescaped pipes and preserves escaped pipe characters in cells. Audit readers use strict separator validation, then require the columns recognized by their particular record extractor. This is a small pipe-table parser rather than a complete Markdown syntax engine. Fenced examples and comments are not removed by `table_blocks`; keep operational records separate from explanatory code blocks. The special fence/comment handling in `_closeout_questions` applies only to governance prompts. [scripts/validate_templates.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/validate_templates.py#L26-L125)

Generated report markers are used to avoid re-ingestion, but exact marker rules differ among readers. Write reports outside the input record directory and retain the original inputs, policy files and audit date together. [scripts/summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/summarize_status.py#L85-L91) [scripts/audit_completeness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_completeness.py#L204-L226) [scripts/audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_punch_list.py#L125-L133)

## Record relationships

| Relationship | Executable check | What remains external |
| --- | --- | --- |
| Check ID → Evidence IDs → evidence-register entry | Unique/valid IDs, registered references, metadata, accepted evidence for completed checks; orphan evidence is reported | Whether a referenced PDF/ZIP exists, is authentic or proves the criterion |
| Measurement → Instrument IDs → calibration period | Registered instrument, valid dates, exactly one inclusive covering period for completed measurements, accepted calibration state | Instrument metrology, certificate authenticity and measurement accuracy |
| Punch item → residual-risk record → acceptance decision | Allowed classifications, linked deferrals, active risks and release blockers | Signer authority, technical risk acceptability and field verification |
| Document ID → ordered revision history | Revision scheme, supersession, dates, obsolete history and approved latest record | Whether the stored document matches the installed asset |

Sources: [scripts/audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_evidence_traceability.py#L208-L393), [scripts/audit_calibration_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_calibration_traceability.py#L236-L553), [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L317-L621), [scripts/audit_document_control.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_document_control.py#L169-L389).

## Teaching and presentation assets

`docs/index.html` embeds both configuration and a reusable ten-kind teaching engine. This repository selects `model.kind = "security"` and relabels alert counts as evidence findings. Other model branches are callable engine examples; they are not native BESS validators or the selected lesson. `docs/portfolio/` records source-linked learning paths and browser-local progress. Historical artwork and lesson source revisions remain preserved. [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L150-L242) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L305-L335) [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L139-L144) [docs/portfolio/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/portfolio/index.html#L285-L307)

There is no package build step for the native Python scripts. The source uses standard-library imports; CI runs Python 3.12, unit tests and command-line validators. The existing static site is uploaded directly from `docs/`. See [toolchain](../maintainer/TOOLCHAIN_AND_DEPENDENCY_MATRIX.md) and [publication](../maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md).
