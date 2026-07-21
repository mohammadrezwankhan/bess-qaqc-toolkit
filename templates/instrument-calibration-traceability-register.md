# Instrument Calibration Traceability Register

Use this register to prove that measurement instruments used during BESS commissioning had one approved calibration record covering each completed test date.

## Measurement Use Register

| Measurement ID | Check ID | Measurement or Test | Instrument IDs | Test Date | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| MEAS-001 | CHK-001 | Replace with measured commissioning activity | INS-001 | YYYY-MM-DD | Responsible owner | Planned |

## Calibration History Register

Add one row per calibration period. Retain prior periods when an instrument is recalibrated so historical test evidence remains reproducible.

| Calibration ID | Instrument ID | Valid From | Valid Through | Approval Status | Certificate Location |
| --- | --- | --- | --- | --- | --- |
| CAL-001 | INS-001 | YYYY-MM-DD | YYYY-MM-DD | Pending review | Controlled document-system path |

## Control Rules

- Use unique uppercase identifiers ending in digits.
- Record every instrument used when a test depends on more than one device.
- Use ISO `YYYY-MM-DD` dates and preserve superseded calibration periods.
- Complete or accepted tests only when every instrument has exactly one approved calibration covering the execution date.
- Investigate overlapping calibration periods instead of selecting a certificate silently.
