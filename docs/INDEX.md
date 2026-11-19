# BESS QA/QC documentation handbook

This handbook explains the source at **af44c932684dfd120dea05d150cefcc3e47539a0**, reviewed on **2026-11-19**. The repository contains reusable evidence templates, Python record checks and separate browser teaching material. Software results describe documented inputs; engineering acceptance remains a project decision by authorized people. [SAFETY_AND_RESIDUAL_RISK.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/SAFETY_AND_RESIDUAL_RISK.md#L10-L18)

## Choose a route

| Reader | Start here | Then use |
| --- | --- | --- |
| Developer or first-time user | [Setup and reproducibility](developer/SETUP_AND_REPRODUCIBILITY.md) | [Architecture](developer/ARCHITECTURE.md), [interfaces](developer/API_CLI_AND_INTERFACES.md), [worked examples](developer/WORKED_EXAMPLES_AND_LABS.md), [troubleshooting](developer/TROUBLESHOOTING.md) |
| Reviewer of calculations and assumptions | [Equations and derivations](math-and-physics/EQUATIONS_AND_DERIVATIONS.md) | [Parameters and symbols](math-and-physics/PARAMETERS_AND_SYMBOLS.md), [assumptions and limits](math-and-physics/ASSUMPTIONS_AND_LIMITS.md) |
| Maintainer | [Verification evidence ledger](maintainer/VERIFICATION_EVIDENCE_LEDGER.md) | [CI and release playbook](maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md), [toolchain](maintainer/TOOLCHAIN_AND_DEPENDENCY_MATRIX.md), [known failure modes](maintainer/FAILURE_MODES_AND_TECH_DEBT.md), [documentation runbook](maintainer/DOCS_MAINTENANCE_RUNBOOK.md) |
| Repository owner or successor | [Governance and scope](owner/GOVERNANCE_AND_SCOPE.md) | [Recovery](owner/BUS_FACTOR_RECOVERY_RUNBOOK.md), [portfolio integration](owner/PORTFOLIO_INTEGRATION.md), [architecture decision records](owner/ADR/ADR-0000-INDEX.md) |

## Existing material remains canonical

The [README](../README.md) retains the lifecycle catalog and detailed command guide. Keep using the existing [template files](../templates/), [fictional examples](../examples/), and [example policies](../config/). The handbook explains their interfaces and limitations without replacing project-controlled records.

The [2026-11-17 audit](../AUDIT_REPORT.md), [remediation report](../REMEDIATION_REPORT.md), [test report](../TEST_VERIFICATION_REPORT.md) and [safety notice](../SAFETY_AND_RESIDUAL_RISK.md) remain dated source documents. Their historical test counts and audit conclusions describe their own evaluation. Use the new evidence ledger for this handbook's observation and its limits. [AUDIT_REPORT.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AUDIT_REPORT.md#L3-L24)

## Contribution, citation and planning

- [Contributing](../CONTRIBUTING.md) describes the documentation and fixture review path.
- [Security](../SECURITY.md) describes reporting and record-handling boundaries.
- [Citation metadata](../CITATION.cff) preserves the recorded author and MIT license.
- [Changelog](../CHANGELOG.md) distinguishes this unreleased documentation work from historical source material.
- [Roadmap](../ROADMAP.md) proposes measurable work from 2026-11-19 through 2027-11-18.

## Browser material and publication

The [interactive lab](index.html), [native lesson catalog](native-lessons.html), [source-linked learning guide](portfolio/index.html) and [previous-animation gallery](animations/index.html) remain separate learning surfaces. The interactive lab's workload counts do not run Python audits. The existing Pages workflow uploads the static `docs/` directory; Markdown is maintained as GitHub-rendered documentation, reached through the handbook link on the lab. Deployment of this documentation revision must be verified after merge. [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L139-L144) [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82)
