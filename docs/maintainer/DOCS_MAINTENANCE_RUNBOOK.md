# Documentation maintenance runbook

[Handbook](../INDEX.md) · [Verification ledger](VERIFICATION_EVIDENCE_LEDGER.md) · [Owner scope](../owner/GOVERNANCE_AND_SCOPE.md)

## Canonical map

[docs/INDEX.md](../INDEX.md) is the handbook entry point. The root README retains its project overview and practical history. Developer pages explain use and implementation; science pages describe discrete rules and teaching models; maintainer pages record verification/delivery; owner pages define boundaries/recovery. The [roadmap](../../ROADMAP.md) contains proposals.

Historical audit reports, the archived README, citation metadata, native lesson source pins, and portfolio provenance remain preserved. They are not duplicate current manuals to overwrite during a refresh.

## Change-to-document mapping

| Changed source | Review |
|---|---|
| Python declaration, CLI parser, dataclass, output | Interface catalog, examples, verification entry |
| Parser or source-selection behavior | Architecture, troubleshooting, assumptions, findings |
| Policy vocabulary or template headers | Examples, compatibility discussion, owner adaptation |
| Native audit predicate | Discrete-rule explanation, limits, verification criteria |
| Browser model, parameter, metric, checkpoint | All science pages, worked lessons, tolerances |
| Workflow job, trigger, action, permission, deployment | Toolchain, release and recovery runbooks |
| Authorship, license, actual release | CFF validation, changelog, rights evidence |
| Approved responsibility or reporting channel | Owner scope, recovery, SECURITY.md |
| Proposal implemented | Roadmap status, current behavior docs, tests, changelog |

## Update procedure

1. Pin the source and enumerate its complete tree, including hidden files, data, assets, and directories. Give indexed-only/excluded material an explicit reason; enumeration is not semantic analysis.
2. Read source and existing documentation, preserving authorship, license and history. Record uncertainty instead of inventing missing facts.
3. Inventory public interfaces separately from file coverage: functions/dataclasses, constants, CLI options, browser exports, and top-level scripts with import side effects.
4. Write concrete commands and immutable source references with line ranges. Before a new file has a commit, bind its review to a content fingerprint.
5. Verify local links/headings, tables, source bounds, CFF and executed commands. External availability is a separate check.
6. Inspect the full diff for unauthorized application, policy, test, model, or dependency changes.
7. Obtain independent review and required repository checks; retain candidate, merge, and deployment identity mappings.
8. Update changelog and roadmap statuses from observed outcomes.

## Scientific review

For each formula or predicate, identify source, inputs, units, sign convention, assumptions, initial/boundary conditions where applicable, and validity limits. Label explanatory derivations. Keep local symbols explicit across the ten browser branches; distinguish minutes/hours/seconds/cycles, rates/counts, and display precision/checkpoint tolerance.

The active lesson is uncalibrated. Its tolerance is not measurement uncertainty. For native rules, explain recognized input schemas and exactly which separate auditors execute; a stronger condition in one command is not inherited by another automatically.

## Citation and changelog hygiene

Validate [CITATION.cff](../../CITATION.cff) against declared CFF 1.2.0. Preserve recorded name, ORCID, URL, and MIT declaration absent authoritative corrections. Do not invent authors, DOI, version, release date, security contact or support promise. [CITATION.cff](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/CITATION.cff#L1-L16)

Released entries require actual tags/releases/commits. Preserve audit history as audit history. Unreleased documentation belongs under Unreleased.

## Public evidence hygiene

Use synthetic or approved redacted examples. Exclude credentials, personal signatures, proprietary drawings, contract details and client identifiers from public issues and fixtures. Evidence-location metadata does not imply permission to publish the underlying record. Existing contribution rules require project-neutral changes without confidential project information. [CONTRIBUTING.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/CONTRIBUTING.md#L3-L20)

Keep raw logs and operational review records outside the checkout unless a selected sanitized excerpt is useful public evidence. Public claims need public-safe references.

## Review record

Capture source SHA; candidate SHA or content fingerprint; changed files; environment and commands; exit codes; sanitized logs; source citations; findings; independent reviewer; merge identity; and deployment run/artifact/URL where applicable. Distinguish not-run, unknown, blocked, and not-applicable outcomes.

This is a proposed repeatable handbook-maintenance practice. Existing [AGENTS.md](../../AGENTS.md) CI integrity instructions still govern workflow edits. [AGENTS.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AGENTS.md#L1-L3)
