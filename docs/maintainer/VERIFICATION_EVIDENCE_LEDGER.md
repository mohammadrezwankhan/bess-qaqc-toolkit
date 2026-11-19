# Verification evidence ledger

[Handbook](../INDEX.md) · [Release playbook](CI_CD_AND_RELEASE_PLAYBOOK.md) · [Limits](../math-and-physics/ASSUMPTIONS_AND_LIMITS.md)

## Revision and evidence types

The analyzed source is `af44c932684dfd120dea05d150cefcc3e47539a0`. A local baseline was observed on **2026-11-19**, using **CPython 3.12.14 on Linux** in an isolated virtual environment, before authoring the handbook. The native suite reported **180 tests, OK**, and all eleven commands below exited 0. This is an observed source-baseline result, not a claim about a later PR, merge, deployment, engineering project, or field installation.

The source's earlier audit and test reports describe their own dated revisions and a 176-test result. They are preserved as historical evidence. Do not replace their totals with the newer baseline total. [AUDIT_REPORT.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AUDIT_REPORT.md#L1-L24) [TEST_VERIFICATION_REPORT.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/TEST_VERIFICATION_REPORT.md#L1-L30)

| Evidence category | How to interpret it |
|---|---|
| Implemented behavior | A source permalink and line range shows what the code does |
| Declared configuration | A workflow, example policy, or lesson setting declares an intended input or route |
| Observed execution | A command, environment, revision/fingerprint, time, exit code, and retained output show what ran |
| Proposal | A roadmap item or suggested operating procedure still requires a reviewed change or owner decision |
| Unknown | No current observation establishes the fact; do not convert it into a passing result |

The task's operational verification record retains exact command arrays, timestamps, sanitized stdout/stderr, and content hashes. A final working-tree check must be associated with its content fingerprint in the review record; after committing, record the candidate SHA and remote run URLs separately. The source permalink alone does not prove an execution result.

## Observed source-baseline commands

All commands ran from the repository root with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`. `python` selected the isolated CPython 3.12.14 interpreter. Outputs were captured outside the checkout. Explicit dates reproduce fictional fixtures; they are not a recommendation to assess a real project against those dates.

### B01 — Native unit suite

```bash
python -m unittest discover -s tests -v
```

Observed exit 0, PASS. The captured unittest summary is `Ran 180 tests` followed by `OK`.


### B02 — Strict template governance

```bash
python scripts/validate_templates.py --strict-governance
```

Observed exit 0, PASS. Validated all 35 source templates.


### B03 — Template completeness

```bash
python scripts/audit_completeness.py templates --policy config/readiness-completeness-policy.example.json
```

Observed exit 0, PASS.


### B04 — Readiness passing record

```bash
python scripts/audit_readiness.py examples/readiness-gate-passing-record.md --status-policy config/readiness-status-policy.example.json --completeness-policy config/readiness-completeness-policy.example.json --as-of 2026-07-21 --require-source-coverage
```

Observed exit 0, PASS.


### B05 — Lifecycle worked example

```bash
python scripts/audit_readiness.py examples/lifecycle-worked-example.md --status-policy config/readiness-status-policy.example.json --completeness-policy config/readiness-completeness-policy.example.json --as-of 2026-01-15 --require-source-coverage
```

Observed exit 0, PASS.


### B06 — Evidence traceability

```bash
python scripts/audit_evidence_traceability.py examples/commissioning-evidence-traceability-passing.md
```

Observed exit 0, PASS.


### B07 — Calibration traceability

```bash
python scripts/audit_calibration_traceability.py examples/calibration-traceability-passing.md
```

Observed exit 0, PASS. This invocation omits optional `--as-of`, matching the configured maintenance workflow; it does not exercise that option's future-completed-measurement cutoff.


### B08 — Punch-list closeout

```bash
python scripts/audit_punch_list.py examples/punch-list-closeout-passing.md --as-of 2026-07-21
```

Observed exit 0, PASS.


### B09 — Handover acceptance

```bash
python scripts/audit_handover_acceptance.py examples/handover-acceptance-passing.md --policy config/handover-acceptance-policy.example.json
```

Observed exit 0, PASS.


### B10 — Document control

```bash
python scripts/audit_document_control.py examples/document-control-passing.md --as-of 2026-07-21
```

Observed exit 0, PASS.


### B11 — Portfolio guide integrity

```bash
python scripts/portfolio/validate_guide.py
```

Observed exit 0, PASS. The validator reported four source-linked paths; it checked embedded guide configuration, local source-path existence, SVG XML, and the configured source pin.


## Claim-to-test map

| Claim or risk | Existing check / source | Passing criterion and limit |
|---|---|---|
| Pipe table and governance structure | [tests/test_validate_templates.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_validate_templates.py#L1-L32); strict template command | Expected structure and required governance questions; does not validate engineering truth |
| Status rules and bounded source selection | [tests/test_summarize_status.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_summarize_status.py#L1-L30) | Fixture expectations for parsing, policy, aliases, and path handling |
| Calendar deadline classification | [tests/test_audit_deadlines.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_deadlines.py#L1-L30) | Expected states for explicit dates; no field schedule verification |
| Conditional field completeness | [tests/test_audit_completeness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_completeness.py#L1-L30) | Expected rule matches and missing-field findings |
| Combined readiness behavior | [tests/test_audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_readiness.py#L1-L30) | Selected component results; optional coverage retains the record-derived limitation |
| Check-to-evidence relationships | [tests/test_audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_evidence_traceability.py#L1-L30) | Expected ID, metadata, acceptance, and orphan findings; no evidence-file authentication |
| Calibration history | [tests/test_audit_calibration_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_calibration_traceability.py#L1-L30) | Expected interval, status, measurement-date, and reference outcomes |
| Independent critical closeout wording | [tests/test_audit_punch_list.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_punch_list.py#L1-L30) | Structured verifier and owner comparison; no identity assurance |
| Residual-risk and acceptance joins | [tests/test_audit_handover_acceptance.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_handover_acceptance.py#L1-L30) | Expected cross-record rules; does not inherit punch verifier or calendar parsing |
| Revision chronology | [tests/test_audit_document_control.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_document_control.py#L1-L30) | Expected revision scheme, accepted current record, chronology, and supersedes chain |
| Governance cross-checks and table structure | [tests/test_governance_matrix.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_governance_matrix.py#L1-L30); [tests/test_audit_table_structure.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/tests/test_audit_table_structure.py#L1-L30) | Existing shared-fixture and table-shape expectations |
| Static portfolio guide | [scripts/portfolio/validate_guide.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/portfolio/validate_guide.py#L1-L33) | Declared local source paths and embedded data remain consistent |

The specific assertion inventory is maintained in the operational review record. An executed test count is not a coverage percentage; no branch-coverage, mutation-coverage, browser accessibility, or field-validation percentage is asserted.

## Additional diagnostic observations

Three narrowly scoped diagnostics reproduced existing behavior at this source revision:

1. A readiness input containing one valid record file and one file with no recognized tables passed optional source coverage while reporting only the recognized source.
2. An otherwise passing handover record with a nonblank invalid approval date produced no handover findings.
3. A closed Critical item with generic nonblank closeout notes in the handover fixture produced no handover findings; that auditor does not call the dedicated punch verifier predicate.

These observations establish documented limitations. They are not regression tests committed to the repository, and a “no findings” result in these diagnostics is not endorsement of the record. Their inputs, outputs, and source references are retained in the operational diagnostic receipt. See [current failure modes](FAILURE_MODES_AND_TECH_DEBT.md) and the [roadmap](../../ROADMAP.md).

## Observed remote source checks

A GitHub API observation on **2026-11-19 at 12:44:17 UTC** returned the following completed checks for the exact analyzed source SHA:

| Check | Reported result | Immutable run/job record |
|---|---|---|
| `link-check` | success; completed 2026-11-18 12:12:03 UTC | [Run 44301612596, job 134792481846](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/actions/runs/44301612596/job/134792481846) |
| `human-authorship-policy` | success; completed 2026-11-18 12:11:59 UTC | [Run 44301612464, job 134792481754](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/actions/runs/44301612464/job/134792481754) |

These are remote **source** checks. They do not assert that the authored documentation candidate, a merge queue revision, or a deployed artifact has passed. The local 180-test observation is independently recorded above; check-run metadata alone does not reproduce its stdout.

## Candidate and delivery checks

| Check | Evidence required | Scope |
|---|---|---|
| Native commands above | Final candidate SHA or working-tree fingerprint, exact commands, exit codes, sanitized logs | Preserves observed native behavior |
| Markdown navigation | Parsed local links and heading anchors for new handbook files; review existing HTML-linked content | Local targets, not availability of every external URL |
| Citation metadata | `CITATION.cff` validated against its declared CFF 1.2.0 schema | Structure, not a new author or DOI claim |
| Source-reference bounds | Every authored permalink matches an existing pinned file and valid line range | Locator integrity, followed by semantic review |
| Change scope | File-level diff and hashes; unchanged scripts, tests, policies, workflows, lesson data | Documentation scope |
| Browser navigation | Unchanged scripts and existing styles plus a functioning handbook link | Narrow navigation addition |
| Remote CI | Actual required checks, tested revision kind, run URLs and conclusion | Local PASS does not replace remote integration evidence |
| Published Pages | Deployment run/artifact provenance, URL, served content, merged-source mapping | Hosting outcome after merge |

A skipped, missing, inaccessible, historical, or neutral check is not an executed PASS. Preserve mappings from synthetic merge or merge-queue revisions to their head and base. Never rewrite the evidence to imply checks ran against a different tree.

## Engineering validation remains external

Native record predicates and synthetic lesson comparisons are software verification. Engineering validation requires the relevant project evidence, test methods, calibrated instruments, competent reviewers, contractual acceptance rules, and authorized decisions. Those external facts are not supplied or certified by this ledger.
