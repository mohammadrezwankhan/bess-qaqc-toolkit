# Contributing

Contributions should improve practical BESS QA/QC clarity.

## Good Contributions

- Add checklist items with clear acceptance evidence.
- Improve FAT/SAT terminology.
- Add document-control fields.
- Clarify commissioning readiness gates.

## Pull Request Checklist

- [ ] The change is project-neutral.
- [ ] The evidence requirement is clear.
- [ ] No confidential project information is included.
- [ ] Markdown tables render cleanly.
- [ ] `python scripts/validate_templates.py` passes.
- [ ] `python -m unittest discover -s tests -v` passes for script changes.
- [ ] Evidence IDs resolve to the controlled register when an evidence matrix changes.

## Documentation and evidence workflow

Start with the [handbook](docs/INDEX.md) and [documentation maintenance runbook](docs/maintainer/DOCS_MAINTENANCE_RUNBOOK.md). Cite immutable source commits and line ranges for behavior claims, distinguish implemented behavior from proposals, and preserve dated audit reports and known citation authorship.

For documentation changes, verify local targets/anchors and the relevant command examples. Record the exact source/candidate identity, environment, exit codes and sanitized output. The [verification ledger](docs/maintainer/VERIFICATION_EVIDENCE_LEDGER.md) lists the existing commands; use its explicit fixture dates when reproducing examples.

Keep application, policy and teaching-model changes in a clearly reviewed scope. A prose change must not silently change acceptance rules, source selection, expected test outcomes or checkpoint tolerances. Report demonstrated limits in [failure modes](docs/maintainer/FAILURE_MODES_AND_TECH_DEBT.md) and propose measurable follow-up in the [roadmap](ROADMAP.md).

Preserve the [AGENTS.md](AGENTS.md) CI instructions, existing workflow contexts and repository protections. Use accurate authorized authorship and an accepted signed-commit route; do not fabricate identity or weaken checks. See the [release playbook](docs/maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md) for current observed controls.

Use synthetic or approved redacted records. For potentially sensitive vulnerabilities or exposed data, follow [SECURITY.md](SECURITY.md) rather than posting details in a public issue.
