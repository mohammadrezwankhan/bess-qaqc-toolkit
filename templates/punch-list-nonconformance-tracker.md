# Punch-List and Nonconformance Tracker

Use this tracker to manage BESS punch-list items, nonconformances, owner actions, and closeout evidence during commissioning and handover.

## Tracker

| ID | Severity | Finding or Nonconformance | System Area | Owner | Evidence Link | Target Close Date | Status | Verification / Closeout Note |
|---|---|---|---|---|---|---|---|---|
| PL-001 | Major | PCS enclosure grounding label missing on unit PCS-02 | PCS | Electrical supervisor | Photo log / inspection sheet | 2026-08-15 | Open | Verify replacement label, photo evidence, and as-built tag list update. |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

## Severity Guide

| Severity | Use When | Typical Closeout Evidence |
|---|---|---|
| Critical | Safety, protection, fire interface, or grid interconnection risk blocks energization or operation. | Corrective action record, approved retest, responsible engineer sign-off. |
| Major | Reliability, warranty, performance, or contractual closeout is affected but work can continue under control. | Inspection record, updated document, photo evidence, or retest result. |
| Minor | Documentation, labeling, workmanship, or housekeeping issue does not affect safe operation. | Photo evidence, corrected document, or owner confirmation. |

## Status Values

| Status | Meaning |
|---|---|
| Open | Issue is logged and awaiting owner action. |
| In progress | Corrective action is underway. |
| Ready for verification | Owner says the action is complete and evidence is available. |
| Closed | Independent reviewer accepted the evidence and closeout note. |
| Deferred | Item is accepted for later closeout with approved residual risk and owner. |

Custom policies that use `In progress` or `Ready for verification` must
classify those values as open punch statuses.

For a closed Critical item, link the approved verification record and enter
`Verified by: <independent reviewer>; Result: Passed` in the closeout-note
column. Replace the placeholder with the recorded name or role of a reviewer
other than the item owner.

## Review Cadence

- Review critical and major items daily during commissioning windows.
- Keep every item tied to a named owner and a target close date.
- Link evidence directly; avoid private notes that cannot be audited later.
- Separate accepted deferrals from unresolved punch-list work.
- Capture repeated issues as trend items for supplier or construction feedback.

## Closeout Questions

- What evidence would defend this decision in a later audit?
- Does the finding affect safety, energization, warranty, grid compliance, or documentation?
- Who owns the next action, and when is it reviewed?
- What unresolved residual risk must appear in the final acceptance package?
- Does the evidence prove the issue is fixed, not only acknowledged?
- Has any affected drawing, test record, asset tag, or procedure been updated?
