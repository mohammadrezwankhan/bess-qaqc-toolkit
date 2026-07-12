# Acceptance Evidence Wording Guide

Use this guide to turn inspection notes, screenshots, certificates, and deviation comments into acceptance evidence that can be reviewed later without private context.

## Weak vs Strong Wording

| Evidence Type | Weak Wording | Stronger Wording |
|---|---|---|
| Screenshot | Screenshot attached. | SCADA screenshot `SCADA-BMS-2026-08-12-01` shows all 24 battery racks online at 2026-08-12 14:05 local time with no active BMS communication alarms. |
| Test record | Test passed. | SAT record `PCS-FUNC-003`, Rev B, shows PCS-01 followed 0 kW to 500 kW discharge and 500 kW to 0 kW stop commands within the approved ramp-rate limit. |
| Certificate | Certificate received. | Meter calibration certificate `MTR-CAL-117` is valid through 2027-03-31 and matches revenue meter serial number `RM-02` in the handover index. |
| Deviation note | Minor issue accepted. | Deviation `NC-014` for missing auxiliary label was accepted by the commissioning manager on 2026-08-14, with replacement label due before final handover. |

## Evidence Checklist

| Question | Why It Matters |
|---|---|
| Does the wording identify the asset, system, or tag? | Reviewers need to know what the evidence proves. |
| Does it include date, revision, or test record reference? | Acceptance evidence should be traceable to a controlled source. |
| Does it state the acceptance condition, not only the activity performed? | "Checked" is weaker than "meets the approved criterion." |
| Does it name unresolved deviations or residual risk? | Hidden exceptions can become handover disputes. |
| Can an independent reviewer understand it without asking the field team? | Good closeout evidence should survive team turnover. |

## Practical Writing Pattern

Use this sentence shape when evidence quality matters:

```text
[Evidence artifact] shows [specific asset/system] met [acceptance criterion] on [date/time or revision], with [exceptions or residual risk].
```

## Closeout Tips

- Prefer record IDs, tag IDs, serial numbers, drawing revisions, and timestamps over broad phrases.
- Describe what the evidence proves, not just that a file exists.
- Keep deviation wording factual and separate from blame.
- Link related punch-list or nonconformance IDs when acceptance is conditional.
- Update the handover document index when evidence changes after final review.
