# Commissioning Evidence Review Examples

Use these examples to review whether commissioning evidence is accepted, rejected, or accepted conditionally with a tracked residual risk.

## Review Examples

| Evidence Type | Evidence Submitted | Review Outcome | Reason | Follow-Up |
|---|---|---|---|---|
| Screenshot | SCADA screenshot shows all BMS racks online with timestamp, asset name, and no active communication alarms. | Accepted | Evidence proves the stated acceptance condition and is traceable. | Add screenshot ID to the [commissioning evidence matrix](commissioning-evidence-matrix.md). |
| Screenshot | Cropped image labeled "BMS OK" without timestamp or visible system identifier. | Rejected | Reviewer cannot confirm date, asset, or alarm state. | Resubmit full screenshot using the [acceptance evidence wording guide](acceptance-evidence-wording-guide.md). |
| Test record | PCS command-following test record includes command source, ramp response, pass/fail result, and signed approver. | Accepted | Test result is complete and tied to the procedure. | Add record ID to the [handover document index](handover-document-index.md). |
| Certificate | Meter calibration certificate is valid but references a serial number that does not match the handover index. | Conditional | Certificate may be valid, but traceability is unresolved. | Track mismatch in the [punch-list tracker](punch-list-nonconformance-tracker.md). |
| Deviation | Minor label issue accepted by owner with interim control and target close date. | Conditional | Deferred work is acceptable only with owner, interim control, and closeout evidence. | Add to the [residual-risk acceptance template](residual-risk-acceptance-template.md). |
| Deviation | Protection settings mismatch marked "will fix later" with no owner or approval. | Rejected | Safety and grid-interface risks cannot be deferred informally. | Block hold point until approved evidence is provided. |

## Reviewer Rule

Accepted evidence should prove the acceptance condition. Conditional evidence should name the residual risk, owner, interim control, and target close date. Rejected evidence should state the missing traceability or acceptance gap clearly enough that the submitter can fix it.
