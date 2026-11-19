# Worked examples and labs

[Handbook index](../INDEX.md)

All records below are teaching fixtures. A clean software report checks documented structure and relationships; it does not verify a real BESS installation, certificate, test result or signature. [examples/lifecycle-worked-example.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/lifecycle-worked-example.md#L5-L11) [examples/punch-list-closeout-passing.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/punch-list-closeout-passing.md#L13-L14)

## Lab 1: inspect a combined readiness report

```bash
python scripts/audit_readiness.py examples/lifecycle-worked-example.md \
  --status-policy config/readiness-status-policy.example.json \
  --completeness-policy config/readiness-completeness-policy.example.json \
  --as-of 2026-01-15 --require-source-coverage --format json
```

The seven lifecycle rows include closed/approved work and four active actions with future deadlines relative to 2026-01-15. Inspect `gate`, the three named entries in `checks`, and `checks.source_coverage`. The corresponding fixture audit returned exit 0 in the 2026-11-19 Python 3.12.14 observation. This is a retrospective fixture date, not a claim that its open work is current. [examples/lifecycle-worked-example.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/lifecycle-worked-example.md#L13-L21) [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L208-L240)

For a controlled negative exercise, copy the example outside the repository, remove one active action's owner, and run the same policies against that copy. The completeness rule requires an accountable owner for its matching active states. Expect a line-located finding and exit 2; retain the unchanged original for comparison. This exercise describes existing rule behavior, not a newly supplied project record. [config/readiness-completeness-policy.example.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/config/readiness-completeness-policy.example.json#L8-L34)

## Lab 2: run the specialized gates

Run from the repository root:

```bash
python scripts/audit_evidence_traceability.py \
  examples/commissioning-evidence-traceability-passing.md --format json
python scripts/audit_calibration_traceability.py \
  examples/calibration-traceability-passing.md --format json
python scripts/audit_punch_list.py \
  examples/punch-list-closeout-passing.md --as-of 2026-07-21 --format json
python scripts/audit_handover_acceptance.py \
  examples/handover-acceptance-passing.md \
  --policy config/handover-acceptance-policy.example.json --format json
python scripts/audit_document_control.py \
  examples/document-control-passing.md --as-of 2026-07-21 --format json
```

The corresponding existing CI audits returned exit 0 in the local observation. JSON is the existing alternate presentation format; the same audit logic supplies it. [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L65-L97)

| Fixture | Inspect | Interpretation |
| --- | --- | --- |
| Evidence traceability | Shared `EVD-002`, registered evidence and approval states | Shared evidence is allowed; unknown, duplicate and orphan references are reported |
| Calibration | Two periods for `INS-001`; a planned 2028 measurement | Inclusive historical coverage is checked for completed measurements; a planned test can lie outside calibration history |
| Punch list | Closed Critical item and independent reviewer wording | The syntax and distinct recorded verifier are checked, not a real person's identity |
| Handover | `PL-002` → `RR-001` → `ACC-001` | Conditional acceptance enumerates active residual risks |
| Document control | Alphabetic `HND-101` and numeric `HND-102` histories | Each document retains one revision scheme and an approved latest record |

Sources: [examples/commissioning-evidence-traceability-passing.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/commissioning-evidence-traceability-passing.md#L7-L17), [examples/calibration-traceability-passing.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/calibration-traceability-passing.md#L7-L26), [examples/punch-list-closeout-passing.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/punch-list-closeout-passing.md#L6-L14), [examples/handover-acceptance-passing.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/handover-acceptance-passing.md#L7-L25), [examples/document-control-passing.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/document-control-passing.md#L7-L12).

The calibration command above follows CI and leaves `--as-of` unset. Add a declared audit date when future completed-test detection is required; that control is conditional on `as_of` being supplied. [scripts/audit_calibration_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_calibration_traceability.py#L236-L553)

## Lab 3: build a project-specific record set

Choose the actual lifecycle templates from the [README catalog](../../README.md#toolkit-contents), copy them into controlled project storage, and replace example IDs, placeholders, dates, statuses and locations. Review the example policies against the actual column headings before running a gate. The supplier tracker lists some states that are not in the example `Review Status` allowlist; the policy must be deliberately agreed rather than silently weakened to get a pass. [templates/supplier-document-review-tracker.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/templates/supplier-document-review-tracker.md#L13-L20) [config/readiness-status-policy.example.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/config/readiness-status-policy.example.json#L25-L35)

Do not run every audit over every template indiscriminately. Some files are human review prompts rather than machine-readable registers, and unfinished starter records are intentionally incomplete. Use matching examples to understand each extractor's table signature. Maintain an explicit input manifest: `--require-source-coverage` compares recognized sources across the three readiness controls, not every supplied file. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L78-L113) [scripts/audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_handover_acceptance.py#L245-L310)

## Lab 4: synthetic review capacity

Open the [interactive lab](../index.html). Load a lesson preset and inspect its 60-minute checkpoint.

| Preset | Arrivals/min | Reviewers | Findings/min/person | Assumed triage | Derived checkpoint |
| --- | ---: | ---: | ---: | ---: | --- |
| Module 1 | 12 | 2 | 4 | 0% | Backlog 240; coverage about 66.6667% |
| Module 2 | 12 | 3 | 4 | 0% | Backlog 0; coverage 100% |
| Module 3 | 20 | 3 | 4 | 0% | Backlog 480; coverage 60% |
| Module 4 | 20 | 3 | 4 | 40% | Processed findings 1,200; coverage 100% |

These values are analytical consequences of the configured constant-rate model and declared fixtures, not measured staffing performance. Each configured numerical checkpoint uses tolerance 0.02 in its metric's units. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L146-L305) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L305-L333)

Exported synthetic counts cannot replace the native reports or controlled human acceptance. The [equations](../math-and-physics/EQUATIONS_AND_DERIVATIONS.md) explain why zero backlog and complete engineering evidence are different quantities.
