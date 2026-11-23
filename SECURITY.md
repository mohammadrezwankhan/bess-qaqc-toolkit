# Security and sensitive reporting

## Scope

This project reads local Markdown/JSON records and writes local reports; its static browser lesson performs synthetic calculations. It does not control equipment or authenticate project evidence. Treat repository security, confidential project information, and actual engineering acceptance as distinct responsibilities. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506) [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L129-L144)

No supported-version window, security response SLA, dedicated security email or verified private disclosure contact was declared in the inspected source. This policy does not invent those commitments.

## Reporting a problem

For a **non-sensitive reproducible software defect**, use the [repository issue tracker](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/issues), including the source revision, command, Python version, expected/actual result and a synthetic minimal fixture.

For a **sensitive vulnerability or exposed information**, open [GitHub Security Advisories](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/security/advisories) and select **Report a vulnerability**. If no verified private channel is available, request one from the maintainer using a non-sensitive message and withhold exploit details, credentials, client records and personal information from public issues. Do not assume a public issue or an unverified email address is private.

Repository access and account/signing recovery remain with the authorized owner. This document records no guaranteed response time or acceptance of a report.

## Handling project records

- Use fictional or properly authorized redacted fixtures in public reports.
- Keep credentials, private signing material, certificates with personal details, proprietary drawings, client names and commercial information out of public commits and logs.
- Preserve the actual evidence and authorization trail in the controlled project system.
- Treat a populated evidence-location field as a reference to inspect, not proof that a file exists or is authentic.
- Select an output directory deliberately: source-path checks do not prevent overwriting the caller's chosen output path.

Existing confidentiality rule: [CONTRIBUTING.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/CONTRIBUTING.md#L12-L20). Evidence metadata checks: [scripts/audit_evidence_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_evidence_traceability.py#L208-L393). Report writing: [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506).

## Supply-chain and repository controls

The source pins GitHub Actions to full commits and gives read-only permissions to validation jobs. Pages deployment separately requests pages/id-token write permissions. Preserve these controls and the active signed-commit rules; do not disable a check or broaden credentials to hide a failure. [AGENTS.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AGENTS.md#L1-L3) [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82)

The known record-validation gaps are documented in [failure modes](docs/maintainer/FAILURE_MODES_AND_TECH_DEBT.md). A passing readiness or browser checkpoint is not a security certification, physical safety approval, or authorization to energize equipment.

## Maintainer follow-up

An owner should assign recovery responsibility before promising support. Record any approved channel and support policy with its actual effective date. The [owner runbook](docs/owner/BUS_FACTOR_RECOVERY_RUNBOOK.md) identifies the current recovery gaps.
