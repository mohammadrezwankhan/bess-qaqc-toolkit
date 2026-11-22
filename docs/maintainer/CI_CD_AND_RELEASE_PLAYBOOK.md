# CI/CD and release playbook

[Handbook](../INDEX.md) · [Verification ledger](VERIFICATION_EVIDENCE_LEDGER.md) · [Recovery](../owner/BUS_FACTOR_RECOVERY_RUNBOOK.md)

## Configured GitHub Actions workflows

This table describes workflow files at source revision `af44c932684dfd120dea05d150cefcc3e47539a0`. Configuration does not by itself establish run success or current repository rules.

| Workflow / producing job | Triggers and selection | Configured work | Permissions / timeout |
|---|---|---|---|
| Markdown maintenance / `link-check` | Manual; PRs and main pushes for Markdown, scripts, tests, config, or its workflow | Python 3.12 tests, strict templates, completeness, readiness, specialized audits, Lychee | Contents read; 20 min |
| Flagship dashboard / `validate` then `deploy` | Manual; main pushes for docs, assets, or its workflow | Static identity/config checks; upload `docs`; publish Pages on main after validation | Validation contents read, 5 min; deploy contents read plus pages/id-token write, 10 min |
| Portfolio guide checks / `validate` | PRs and main pushes use scoped portfolio path filters; all tag pushes trigger | Run `scripts/portfolio/validate_guide.py` | Contents read; 5 min |
| Human authorship policy / `human-authorship-policy` | PRs, merge groups, main pushes, all tags | Inspect commit metadata over the applicable revision range | Contents read; 5 min |

Sources: [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L1-L104) [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L1-L82) [.github/workflows/portfolio-dashboard-check.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/portfolio-dashboard-check.yml#L1-L24) [.github/workflows/no-codex-attribution.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/no-codex-attribution.yml#L1-L99).

No CircleCI or Buildkite configuration appears in the pinned tree. This does not establish whether an external service is connected through repository settings.

### Coverage nuances

GitHub does not evaluate path filters for tag pushes. The portfolio workflow's all-tags selector therefore applies independently of its path filters, which still apply to the configured PR and branch-push events. See [GitHub's workflow-trigger documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#using-filters-to-target-specific-paths-for-pull-request-or-push-events).

The existing networked Lychee invocation checks `README.md`, `CONTRIBUTING.md`, `examples/*.md`, and `templates/*.md`. A second offline invocation checks relative paths and anchors in the handbook index and the API, architecture, troubleshooting, assumptions, failure-mode, maintenance, and CI playbook pages. This keeps handbook navigation in the existing `link-check` job without extending its network-dependent URL set. Other handbook pages and several root documents remain outside Lychee scope. The native audit steps use fixed example dates, and calibration omits optional `--as-of`. [Current workflow](../../.github/workflows/markdown-maintenance.yml)

Pages validation runs on main push or manual dispatch, not a PR trigger in its current file. Deployment uploads static `docs` without a Markdown site generator. The handbook link therefore points to GitHub-rendered Markdown, rather than presenting raw `.md` files as a new HTML documentation site. [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L6-L12) [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82)

## Observed repository rules

On **2026-11-19 at 12:44:25 UTC**, [ruleset 20091520](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/rules/20091520) was active on **all branches**, required signed commits, listed no bypass actors, and reported no bypass permission for the current actor. The branch API's required-status-check list was empty; that is not absence of protection because the ruleset still applies. Refresh both rule and branch metadata before integration.

Use an authorized signing route and verify the resulting commit's signature status. If the available tool cannot create an accepted signed commit, retain the candidate for an authorized owner to integrate. Do not remove protection, invent a signature, spoof an author, or reinterpret an unsigned write as success. The human-authorship workflow is a separate metadata policy, not a substitute for the signed-commit rule.

## Before changing or merging documentation

1. Read [AGENTS.md](../../AGENTS.md). Preserve required contexts and job names, PR validation, release/publication routes, tag coverage, matrices, security checks, and deployment gates.
2. Pin the source and recheck the remote default-branch head. Reconcile source claims and rerun affected checks if it moved.
3. Inspect the entire candidate diff. A navigation edit must not silently change native predicates, policies, models, teaching data, or tests.
4. Run the [verification ledger](VERIFICATION_EVIDENCE_LEDGER.md) commands and Markdown/CFF/source-reference checks. Associate outputs with the exact candidate identity.
5. Inspect actual rules and required contexts; do not infer them from workflow files alone.
6. Use accurate authorized authorship and the signed-commit route. Disclose tool assistance accurately where required.
7. Obtain independent review, resolve findings, observe checks on the integrated candidate, and use the permitted merge path.

These are instructions, not claims that this candidate has been pushed or merged. CI integrity guidance: [AGENTS.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/AGENTS.md#L1-L3). Metadata policy: [.github/workflows/no-codex-attribution.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/no-codex-attribution.yml#L33-L99).

## Release history and versioning

The API observation on **2026-11-19 at 12:44:17 UTC** returned empty [release](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/releases) and [tag](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/tags) collections. This is a dated observation. The pinned tree contains no package-version manifest or release-publishing workflow. Audit dates and merge commits must not be presented as tagged releases.

For an authorized release, recheck tags/releases, identify the intended previous release and candidate, derive notes from the real comparison, preserve source/check/approval/tag evidence, and verify the resulting release object. Add version/date fields to citation metadata only when the actual release supports them. This handbook does not introduce a release cadence, support window, or versioning promise.

## Pages publication verification

The owner settings observation on **2026-11-19 at 12:45:40 UTC** showed the existing site live at [the repository Pages URL](https://mohammadrezwankhan.github.io/bess-qaqc-toolkit/), with **GitHub Actions** as source and **Flagship dashboard** as the last deployment workflow to `github-pages`. This establishes the configured/live route at that time; it does not establish that this documentation candidate is deployed. The source workflow uploads `docs`. [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82)

After an authorized merge:

1. Record the merged commit and the main-branch workflow run.
2. Confirm validation/deployment conclusions and preserve source/run/artifact/URL mapping.
3. Load the served page, confirm its repository identity and expected content, and follow the “Documentation handbook” link to the merged GitHub-rendered handbook.
4. Record time, URL, content identity, and limits. A pending deployment stays pending.
5. Diagnose validation, environment/permissions, artifact, and serving failures separately.

Historical source pins inside the lesson and portfolio guide do not establish the current deployment revision and should not be automatically retargeted during prose maintenance.

## Failure triage

| Failure | First evidence | Scoped response |
|---|---|---|
| Native audit or unit failure | stderr, input, policy, assessment date, tested SHA | Reproduce exactly; correct the documented assumption or propose a reviewed behavior fix |
| Link failure | Target and source line | Repair the link; do not suppress all failures |
| Portfolio validator failure | Embedded JSON, local paths, SVG parse, source pin | Restore consistency without rewriting unrelated history |
| Signature rejection | Commit verification and current rules | Use an accepted authorized signing route; preserve protection |
| Authorship check rejection | Commit range and rejected metadata | Use truthful authorized identity; preserve the policy |
| Pages validation failure | Marker, JSON, symlink, external-script finding | Repair only the demonstrated documentation artifact defect |
| Pages deployment failure | Environment, permissions, Pages setting, artifact, run logs | Restore the configured route through an authorized owner |

No timeout reduction or CI-cost saving is claimed without an observed successful-run baseline. Existing caps are documented, not modified or newly justified.
