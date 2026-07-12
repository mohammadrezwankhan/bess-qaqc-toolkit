# Commissioning Evidence Matrix

Use this matrix to map BESS commissioning checks to the evidence package needed for project closeout and handover.

| System Area | Check or Test | Required Evidence | Acceptance Reference | Owner | Status |
|---|---|---|---|---|---|
| Battery racks | Visual inspection complete | Signed inspection sheet with photo log and serial-number range | Approved ITP / supplier manual | QA/QC | Not started |
| Battery racks | Torque verification complete | Torque record with tool ID, calibration status, and sampled connection list | Installation procedure | Electrical supervisor | Not started |
| BMS | Rack/module communication verified | BMS screenshot or exported device list showing all expected nodes online | BMS commissioning procedure | Controls engineer | Not started |
| BMS | Alarm and trip mapping verified | Alarm matrix test record with pass/fail result and timestamp | Approved cause-and-effect matrix | Controls engineer | Not started |
| PCS | Pre-energization checks complete | Insulation, grounding, polarity, and auxiliary supply test records | PCS commissioning procedure | Electrical supervisor | Not started |
| PCS | Charge/discharge command test complete | Test log showing command source, power setpoint, response, and ramp behavior | SAT procedure | Commissioning engineer | Not started |
| EMS/SCADA | Remote command interface verified | SCADA screenshots, point-to-point test sheet, and command response log | SCADA point list / EMS procedure | Controls engineer | Not started |
| Fire safety | Emergency stop interface verified | E-stop activation record and reset confirmation | Fire safety interface procedure | HSE / commissioning | Not started |
| Metering | Revenue/settlement meter checked | Meter calibration certificate and point verification record | Metering specification | Grid interface owner | Not started |
| Grid interface | Protection settings verified | Approved settings file, relay upload record, and secondary injection test report | Protection study / grid-code requirement | Protection engineer | Not started |
| Performance | Capacity or functional performance test complete | Test report with raw data, assumptions, correction method, and deviations | Performance test procedure | Commissioning manager | Not started |
| Handover | Punch list closure verified | Punch list export with owner, due date, closure evidence, and residual risk | Handover plan | Project controls | Not started |

## Evidence Quality Rules

- Evidence should be traceable to a drawing, procedure, specification, or acceptance criterion.
- Screenshots should include date, system name, and visible tag or asset identifier where possible.
- Test records should identify instrument ID and calibration validity when measurement accuracy matters.
- Deviations should be captured in a nonconformance or punch-list process, not hidden in free text.

## Closeout Questions

- Is every required evidence item linked to a responsible owner?
- Are open deviations categorized by safety, reliability, performance, documentation, or commercial impact?
- Can an independent reviewer understand the system state without asking the commissioning team for private context?
