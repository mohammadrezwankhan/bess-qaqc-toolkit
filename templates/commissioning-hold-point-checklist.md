# Commissioning Hold-Point Checklist

Use this checklist to manage BESS commissioning gates where work should pause until required evidence, approvers, and release conditions are satisfied.

| Hold Point | Required Evidence | Approver | Release Condition | Status | Notes |
|---|---|---|---|---|---|
| Pre-energization readiness | FAT/SAT records, insulation test results, grounding checks, and open punch-list export | Commissioning manager / electrical lead | No critical open items; required tests complete and reviewed | Not started | Cross-check the [commissioning evidence matrix](commissioning-evidence-matrix.md). |
| Battery rack energization | Rack inspection records, BMS communication proof, torque evidence, and alarm status | Battery lead / controls engineer | All expected racks visible in BMS with no blocking alarms | Not started | Reference [acceptance evidence wording guide](acceptance-evidence-wording-guide.md). |
| PCS first power conversion | PCS pre-checks, protection settings, command path, and emergency stop test | Electrical lead / protection engineer | PCS follows command at approved low-power setpoint | Not started | Capture command source and ramp behavior. |
| EMS/SCADA command release | Point-to-point records, command hierarchy, alarm visibility, and operator access | Controls lead / operations representative | Operator can view state and command only approved functions | Not started | Confirm advisory vs direct-control commands. |
| Performance test start | Approved test procedure, baseline conditions, metering readiness, and deviation list | Commissioning manager / owner representative | Test boundary conditions and acceptance criteria are agreed | Not started | Link residual-risk items if any test proceeds conditionally. |
| Handover release | Handover document index, residual-risk register, punch-list closure, and closeout review | Project manager / operations lead | Operations accepts documents, residual risk, and known limitations | Not started | Use the [closeout review checklist](closeout-review-checklist.md). |

## Reviewer Prompts

- Is every hold point tied to a named approver?
- Is the release condition objective enough to audit later?
- Are blocked, deferred, and accepted-with-risk items separated?
- Are evidence links stored in a controlled location?
- Does the handover package show who accepted any remaining residual risk?
