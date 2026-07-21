# BESS QA/QC Toolkit

[![Markdown maintenance](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/actions/workflows/markdown-maintenance.yml/badge.svg)](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/actions/workflows/markdown-maintenance.yml)

Templates and checklists for battery energy storage system QA/QC, FAT/SAT
readiness, supplier evidence review, and commissioning handover.

## Why This Exists

BESS reliability depends on evidence that can be inspected before energization,
commissioning, and handover. This repository collects practical templates that
help engineering teams make inspection logic easier to review and reuse.

## Planned Contents

- [FAT readiness checklist](templates/fat-readiness-checklist.md).
- [SAT readiness checklist](templates/sat-readiness-checklist.md).
- [Supplier document review tracker](templates/supplier-document-review-tracker.md).
- [Commissioning evidence matrix](templates/commissioning-evidence-matrix.md).
- [Instrument calibration traceability register](templates/instrument-calibration-traceability-register.md).
- [Punch-list and nonconformance tracker](templates/punch-list-nonconformance-tracker.md).
- [Handover document index](templates/handover-document-index.md).
- [Acceptance evidence wording guide](templates/acceptance-evidence-wording-guide.md).
- [Residual-risk acceptance template](templates/residual-risk-acceptance-template.md).
- [BESS closeout review checklist](templates/closeout-review-checklist.md).
- [Commissioning hold-point checklist](templates/commissioning-hold-point-checklist.md).
- [Commissioning evidence review examples](templates/commissioning-evidence-review-examples.md).
- [Document readiness scoring guide](templates/document-readiness-scoring-guide.md).
- [BESS closeout owner map](templates/closeout-owner-map.md).

- [BESS Closeout Timeline Template](templates/closeout-timeline-template.md).

- [Commissioning Shift Handover Log](templates/commissioning-shift-handover-log.md).

- [Warranty Evidence Checklist](templates/warranty-evidence-checklist.md).

- [Fire Safety Interface Review](templates/fire-safety-interface-review.md).

- [Spare Parts Readiness Checklist](templates/spare-parts-readiness-checklist.md).

- [Site Acceptance Risk Register](templates/site-acceptance-risk-register.md).

- [Grid Interconnection Evidence Pack](templates/grid-interconnection-evidence-pack.md).

- [Energization Readiness Gate](templates/energization-readiness-gate.md).

- [O And M Training Record](templates/o-and-m-training-record.md).

- [Defect Aging Summary](templates/defect-aging-summary.md).

- [Supplier Query Log](templates/supplier-query-log.md).

- [Cyber Asset Handover Checklist](templates/cyber-asset-handover-checklist.md).

- [Metering Acceptance Checklist](templates/metering-acceptance-checklist.md).

- [Communication Interface Test Log](templates/communication-interface-test-log.md).

- [Emergency Response Drill Record](templates/emergency-response-drill-record.md).

- [Availability Test Evidence Template](templates/availability-test-evidence-template.md).

- [Environmental Condition Log](templates/environmental-condition-log.md).

- [Relay Settings Review Checklist](templates/relay-settings-review-checklist.md).

- [Site Walkdown Photo Log](templates/site-walkdown-photo-log.md).

- [Final Acceptance Signoff Pack](templates/final-acceptance-signoff-pack.md).

- [Lessons Learned Capture Template](templates/lessons-learned-capture-template.md).

## Repository Topics

```text
bess battery-energy-storage qaqc commissioning fat sat
renewable-energy utility-scale energy-storage
```

## Status

Draft toolkit. Use the templates as starting points and adapt them to
project-specific requirements, standards, and contractual obligations.

## Template Quality Gate

Every template must start with one title and an explanatory paragraph, then
provide at least one structurally valid Markdown table. The repository workflow
checks table separators and column counts in addition to testing links.

Run the same checks locally with Python 3.12:

```powershell
python -m unittest discover -s tests -v
python scripts/validate_templates.py
```

## Readiness Status Roll-Up

After copying and filling project templates, aggregate `Status`, `Review
Status`, and `Approval Status` columns into a reviewable Markdown report:

```powershell
python scripts/summarize_status.py project-records `
  --output project-records\readiness-summary.md
```

Use JSON for another reporting tool, or make a pipeline fail on one or more
project-defined blocking states:

```powershell
python scripts/summarize_status.py project-records --format json
python scripts/summarize_status.py project-records `
  --fail-on Blocked --fail-on Failed
```

The gate compares status names case-insensitively and exits with code `2` when
a configured state occurs. Status-definition tables are excluded from the
roll-up. Running the command without a path summarizes the repository templates.

Use a version-controlled status policy to reject missing values, status typos,
and project-defined blocking states in one reproducible gate:

```powershell
python scripts/summarize_status.py project-records `
  --policy config/readiness-status-policy.example.json `
  --output project-records\readiness-summary.md
```

The JSON policy defines global `allowed_statuses`, `blocking_statuses`, and the
Boolean `require_status` fallback. Optional `column_rules` can assign a complete
replacement rule to headings such as `Approval Status` or `Review Status`, so a
valid state cannot silently appear in the wrong workflow column. Column names
match case-insensitively after whitespace normalization.

Policy violations retain the source file, line, item, status, column, and reason
in Markdown and JSON output; the command exits with code `2` when any violation
is found. Copy and adapt the [example policy](config/readiness-status-policy.example.json)
to the controlled vocabularies and release gates for each project. A matching
column rule replaces rather than merges with the global fallback, keeping each
column's accepted and blocking states explicit.

## Readiness Deadline Audit

Audit dated owner actions separately from status vocabulary. Supply an explicit
`--as-of` date so the same project snapshot produces the same deadline states
in a local review and in CI:

```powershell
python scripts/audit_deadlines.py project-records `
  --as-of 2026-07-21 `
  --output project-records\deadline-audit.md
```

The report classifies each nonblank row as `overdue`, `due_today`, `upcoming`,
`missing`, or `closed`, and preserves its source file, line, item, status,
deadline heading, deadline value, and days to deadline. Use JSON for another
reporting tool, or fail a pipeline on selected states:

```powershell
python scripts/audit_deadlines.py project-records `
  --as-of 2026-07-21 --format json
python scripts/audit_deadlines.py project-records `
  --as-of 2026-07-21 `
  --fail-on overdue --fail-on missing
```

By default, the audit recognizes `Due Date`, `Target Close Date`, and `Required
By` columns. `Accepted`, `Approved`, `Closed`, `Complete`, and `Completed` are
terminal statuses. `TBD`, `TBC`, `N/A`, `NA`, and `-` are controlled missing-date
markers; other nonblank dates must use `YYYY-MM-DD`.

Repeat `--date-column`, `--terminal-status`, or `--missing-date-value` to replace
the corresponding default list for a project. Matching is case-insensitive
after whitespace normalization. Tables with more than one recognized deadline
column and rows with malformed dates fail instead of choosing silently.

## Conditional Completeness Audit

A valid status and deadline do not prove that a readiness row is controlled.
Audit the fields required by each workflow state with a version-controlled JSON
policy:

```powershell
python scripts/audit_completeness.py project-records `
  --policy config/readiness-completeness-policy.example.json `
  --output project-records\completeness-audit.md
```

Each rule selects rows through one-of matching column names and
case-insensitive values, then requires one nonmissing value from every
configured field group. This supports heading variants such as `Owner` or
`Action Owner`, and `Evidence Link` or `Closeout Evidence`, without treating
them as different controls.

The example policy covers active closeout actions, accepted deferrals, and
approved handover documents. It requires the applicable owner, deadline,
approval, revision, and evidence fields while treating `TBD`, `TBC`, `N/A`,
`NA`, and `-` as controlled missing values. Copy and adapt the rule values and
column aliases for each project.

Reports preserve the source file, line, item, matched rule and state, required
field, candidate columns, observed values, and reason in Markdown or JSON. The
command exits with code `2` when violations exist and code `1` for malformed or
ambiguous policies, tables, or a policy that matches no rows. Generated reports
are excluded from later scans.

## Commissioning Evidence Traceability Audit

Cross-check commissioning rows against their controlled evidence register so a
valid status cannot hide an unknown, orphaned, duplicated, or unapproved
evidence record:

```powershell
python scripts/audit_evidence_traceability.py project-records `
  --output project-records\evidence-traceability-audit.md
```

The check table requires a unique `Check ID`, the check or test, one or more
`Evidence IDs`, an acceptance reference, an owner, and a status. The evidence
register requires a unique `Evidence ID`, controlled location, revision, and
approval status. IDs use uppercase hyphenated values ending in digits, such as
`CHK-001` and `EVD-001`; one evidence record may support multiple checks.

`Ready for verification`, `Closed`, and `Accepted` checks require every linked
evidence record to be `Approved` or `Accepted`. Repeat `--completed-status` or
`--accepted-evidence-status` to replace those defaults for a project. Repeat
`--missing-value` to replace the default `TBD`, `TBC`, `N/A`, `NA`, and `-`
placeholders. Matching is case-insensitive, while identifiers remain strict.

Markdown and JSON reports preserve source files, line numbers, check coverage,
register metadata, reverse references, and every finding. The command returns
`0` for a clean audit, `2` for controlled findings, and `1` for malformed input
or missing check/register records. The
[passing example](examples/commissioning-evidence-traceability-passing.md) is
exercised by the repository workflow.

## Instrument Calibration Traceability Audit

Cross-check completed commissioning measurements against dated instrument
calibration history so an evidence package cannot rely on a certificate that
was expired, not yet effective, unapproved, or ambiguous on the test date:

```powershell
python scripts/audit_calibration_traceability.py project-records `
  --as-of 2026-07-21 `
  --output project-records\calibration-traceability-audit.md
```

The measurement-use table links a unique `Measurement ID` and `Check ID` to one
or more `Instrument IDs`, an ISO `Test Date`, owner, and status. The calibration
history retains one row per certificate period with a unique `Calibration ID`,
instrument, `Valid From`, `Valid Through`, approval status, and controlled
certificate location. Multiple nonoverlapping periods for one instrument are
supported so recalibration does not erase historical traceability.

`Complete`, `Completed`, `Accepted`, and `Ready for verification` measurements
require exactly one calibration period per instrument to cover the test date,
and that period must be `Approved`, `Valid`, or `Accepted`. Unknown instruments,
duplicate references and IDs, malformed or reversed dates, coverage gaps, and
overlapping periods are reported with source file and line number. Repeat
`--completed-status`, `--accepted-calibration-status`, or `--missing-value` to
replace the corresponding defaults for a project.
When `--as-of` is supplied, a completed measurement dated after the audit date
is also reported; planned work may still carry a future date.

Markdown and JSON reports preserve measurement coverage, complete calibration
history, reverse instrument references, and every finding. The command returns
`0` for a clean audit, `2` for controlled findings, and `1` for malformed input
or a missing register. The
[passing calibration example](examples/calibration-traceability-passing.md) is
exercised by the repository workflow.

## Punch-List Closeout Audit

Gate a punch-list or nonconformance tracker before verification, deferral, or
handover review:

```powershell
python scripts/audit_punch_list.py project-records `
  --as-of 2026-07-21 `
  --output project-records\punch-list-closeout-audit.md
```

The audit recognizes the tracker fields for unique ID, severity, finding,
system area, owner, evidence link, target close date, status, and verification
or closeout note. It enforces the documented `Critical`, `Major`, and `Minor`
severity vocabulary and the `Open`, `In progress`, `Ready for verification`,
`Closed`, and `Deferred` status lifecycle.

Active rows fail when their ISO target date is overdue. Critical rows must be
terminal and cannot pass as deferred. Verification-ready, closed, and deferred
rows require controlled evidence; terminal rows also require a closeout note.
Malformed dates and identifiers, duplicate IDs, missing controlled values, and
unknown severity or status values remain separate line-level findings.

Markdown and JSON reports preserve source files, row numbers, aggregate status
and severity counts, days to target, overdue state, and every issue. The command
returns `0` for a clean audit, `2` for controlled findings, and `1` for malformed
input or a missing tracker. The
[passing punch-list example](examples/punch-list-closeout-passing.md) is
exercised by the repository workflow.

## Handover Document-Control Audit

Audit the controlled revision history behind a handover package so an approved
document cannot silently replace an earlier issue without a traceable
supersession chain:

```powershell
python scripts/audit_document_control.py project-records `
  --as-of 2026-07-21 `
  --output project-records\document-control-audit.md
```

The register retains one row per document revision. Revisions use either
alphabetic (`Rev A`) or numeric (`Rev 2`) ordering consistently for each
document. Every later issue must name the immediately preceding revision in
`Supersedes Revision`, and its ISO issue date must increase. Historical rows
must be `Superseded` or `Withdrawn`; the latest row must be `Approved`,
`Accepted`, or `Released` and link to its controlled location.

Unknown statuses, duplicate document/revision pairs, inconsistent document
metadata, mixed revision schemes, future issue dates, and broken supersession
chains are reported with source file and line number. Repeat
`--accepted-status`, `--working-status`, `--obsolete-status`, or
`--missing-value` to replace the corresponding defaults. The command returns
`0` for a clean audit, `2` for controlled findings, and `1` for malformed input
or a missing register. The
[passing example](examples/document-control-passing.md) is exercised in CI.

## Handover Acceptance Audit

Cross-check punch-list items, residual-risk approvals, and the signed acceptance
decision before releasing a BESS handover package:

```powershell
python scripts/audit_handover_acceptance.py project-records `
  --policy config/handover-acceptance-policy.example.json `
  --output project-records\handover-acceptance-audit.md
```

The audit requires each deferred punch-list item to resolve to exactly one
active, approved residual-risk record through `Source Item ID`. Closed items
must retain their evidence link and verification note. A conditional acceptance
must enumerate every active residual-risk ID, while an unconditional acceptance
cannot retain any active deferral.

The example policy treats open Critical and Major items as release blockers and
does not permit Critical items to be deferred. Its controlled punch-list and
risk statuses, release decisions, blocker severities, non-deferrable severities,
and missing-value markers are all project-configurable. Policy lists are
validated for duplicates, overlaps, and complete punch-status classification so
a malformed gate fails instead of silently weakening the decision.

Markdown and JSON reports preserve source files, line numbers, all three
registers, aggregate counts, and each cross-register finding. The command
returns `0` for a clean release, `2` for controlled findings, and `1` for a
malformed policy, table, or incomplete register set. The
[passing handover example](examples/handover-acceptance-passing.md) is exercised
by the repository workflow.

## Unified Readiness Gate

Run all three controls as one reproducible release decision when a project
snapshot is ready for review:

```powershell
python scripts/audit_readiness.py project-records `
  --status-policy config/readiness-status-policy.example.json `
  --completeness-policy config/readiness-completeness-policy.example.json `
  --as-of 2026-07-21 `
  --output project-records\readiness-gate.md
```

The combined Markdown or JSON report records each policy source, the explicit
as-of date, selected deadline failure states, source files, per-check result,
counts, line-level findings, and a matrix showing which source files contributed
to each control. It returns `0` only when status policy, deadlines, and
conditional completeness all pass; controlled findings return `2`, while
malformed inputs or a check with no evaluable rows return `1`.

Source coverage is report-only by default because a mixed project folder may
intentionally contain specialized records. When every contributing file is
expected to expose status, deadline, and conditional-completeness rows, enforce
that contract explicitly:

```powershell
python scripts/audit_readiness.py project-records `
  --status-policy config/readiness-status-policy.example.json `
  --completeness-policy config/readiness-completeness-policy.example.json `
  --as-of 2026-07-21 `
  --require-source-coverage `
  --format json
```

Strict coverage creates one finding for every missing source/control pair and
returns `2`. Generated audit reports are excluded from the matrix, so writing a
report inside the scanned directory remains safe for repeat runs.

By default, `overdue` and `missing` deadlines fail the combined gate. Repeat
`--deadline-fail-on` to replace that pair for a project, for example:

```powershell
python scripts/audit_readiness.py project-records `
  --status-policy config/readiness-status-policy.example.json `
  --completeness-policy config/readiness-completeness-policy.example.json `
  --as-of 2026-07-21 `
  --deadline-fail-on overdue --deadline-fail-on due_today `
  --format json
```

The [passing example](examples/readiness-gate-passing-record.md) is exercised in
strict coverage mode by the repository workflow and shows the minimum owner,
deadline, and evidence fields needed by the example policies. Combined reports
can be written inside the scanned directory without being ingested on the next
run.

## Contribution Entry Points

- Add project-specific evidence-traceability examples.
- Add project-specific calibration-history and measurement-use examples.
- Add project-specific handover acceptance policies and records.
- Improve punch-list and nonconformance closeout wording.
- Improve handover document index fields.
- Add project-specific examples to the acceptance evidence wording guide.
- Add project-specific residual-risk acceptance examples.
- Add project-specific closeout review checks.
- Add project-specific commissioning hold points.
- Add more accepted/rejected commissioning evidence examples.
- Add project-specific document readiness scoring examples.
- Add project-specific closeout owner map examples.
- Add project-specific examples to the bess closeout timeline template.
- Add project-specific examples to the commissioning shift handover log.
- Add project-specific examples to the warranty evidence checklist.
- Add project-specific examples to the fire safety interface review.
- Add project-specific examples to the spare parts readiness checklist.
- Add project-specific examples to the site acceptance risk register.
- Add project-specific examples to the grid interconnection evidence pack.
- Add project-specific examples to the energization readiness gate.
- Add project-specific examples to the o and m training record.
- Add project-specific examples to the defect aging summary.
- Add project-specific examples to the supplier query log.
- Add project-specific examples to the cyber asset handover checklist.
- Add project-specific examples to the metering acceptance checklist.
- Add project-specific examples to the communication interface test log.
- Add project-specific examples to the emergency response drill record.
- Add project-specific examples to the availability test evidence template.
- Add project-specific examples to the environmental condition log.
- Add project-specific examples to the relay settings review checklist.
- Add project-specific examples to the site walkdown photo log.
- Add project-specific examples to the final acceptance signoff pack.
- Add project-specific examples to the lessons learned capture template.
