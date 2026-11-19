# Bus-factor recovery runbook

[Handbook](../INDEX.md) · [Governance](GOVERNANCE_AND_SCOPE.md) · [Release playbook](../maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md)

This runbook is a proposed recovery procedure for an authorized replacement maintainer. It does not establish that a deputy already has access. Source and citation identity are known; account recovery, signing material, environment approvals and private reporting contacts require owner-controlled records.

## Minimum handover inventory

| Item | What the owner should preserve | Current evidence / boundary |
|---|---|---|
| Repository and history | Owner/repository URL, default branch, source/release commits and complete history backup | Public source is reproducible at the pinned revision |
| Access and deputy | Actual administrators, authorized deputy and provider recovery route | No deputy roster is declared in source |
| Signing | Approved commit-signing route and recovery procedure | All-branches signed-commit rule observed; never store private signing keys in docs |
| CI | Workflow files, producing jobs, required rules and meaningful passing-run records | Four workflows are tracked; rules/settings are separately observed |
| Pages | Settings, environment, source workflow, latest valid deployment provenance | Existing Actions-to-Pages route observed |
| Releases | Real tags/releases, citation metadata and release notes | Empty tag/release collections observed on 2026-11-19; recheck before release |
| Project evidence | Controlled record locations, permissions, approval authorities and backups | Not reproduced or certified by the public toolkit |
| Reporting channel | Owner-approved sensitive-disclosure method | No verified private contact is established in this handbook |

## Source and behavior recovery

1. Obtain owner-authorized repository access through the provider's normal recovery or delegation process. Do not use another person's session or alter protections to bypass missing authority.
2. Clone or restore the repository into an isolated directory. Verify the selected commit and tracked tree against the preserved record. For the documented snapshot:

```bash
git clone https://github.com/mohammadrezwankhan/bess-qaqc-toolkit.git
cd bess-qaqc-toolkit
git checkout --detach af44c932684dfd120dea05d150cefcc3e47539a0
git rev-parse HEAD
git status --short
```

3. Read [AGENTS.md](../../AGENTS.md), [CITATION.cff](../../CITATION.cff), the license and current rules. Reestablish an authorized signing route and verify the first resulting commit before attempting integration.
4. Create the isolated Python environment described in [setup](../developer/SETUP_AND_REPRODUCIBILITY.md). Run the [verification ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md) commands with the documented fixture dates. Compare expected source behavior; do not overwrite historical evidence.
5. Inspect the current branch head, workflow definitions and dependency pins. If newer source differs from this snapshot, document and test that source separately.
6. Review unresolved findings and [roadmap](../../ROADMAP.md) items before making compatibility-sensitive changes.

These commands restore source, not owner permissions, authentic project data, or a released service.

## CI and publication recovery

The Pages workflow uploads `docs` and uses the `github-pages` environment. It requests contents read, pages write and id-token write for deployment. No user-supplied secret variable name is referenced by the inspected workflows; GitHub-managed authentication and environment permissions are separate from a project API key. Do not invent missing secret names or copy secret values into a recovery note. [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82)

For a failed publication, retain the last known valid deployment provenance, inspect validation/deploy logs, verify Pages source and environment access, and restore the documented route through an authorized change. Re-run deployment only after a reviewed source identity is known. Confirm the served page and handbook link, then record its source/run/artifact mapping.

If rollback is necessary, propose a normal reviewed revert or restore from the identified good commit using the signed-commit and review process. Preserve the failed artifact/run evidence; do not force-rewrite shared history or disable checks to produce a green deployment.

## Project record recovery

Project records need their own controlled backups, retention rules and access permissions. Recover the source documents and policy revisions together with their audit outputs and actual approvals. A regenerated passing report does not recover missing signatures or authenticate a substituted certificate.

Use evidence IDs and source paths to reconstruct relationships, then have authorized reviewers reestablish any missing acceptance evidence. Keep recovered confidential records outside public repository issues.

## Recovery rehearsal and completion criteria

A proposed rehearsal should demonstrate that an authorized deputy can obtain source, verify history, run the existing checks, explain the documented limitations, inspect current rules, and trace a real Pages artifact to its source. It should record unresolved access or reporting-channel gaps without disclosing secret values. See roadmap item BESS-R08.

Completion requires observed results and owner confirmation of the new responsibility assignment. A written runbook alone is not a tested recovery capability.
