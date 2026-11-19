# Portfolio integration

[Handbook](../INDEX.md) · [Architecture](../developer/ARCHITECTURE.md) · [Governance](GOVERNANCE_AND_SCOPE.md)

## Repository role

This repository contributes a document/evidence assurance workflow: templates, controlled records, policy-based Python checks, source-linked examples and a synthetic workload lesson. It does not supply a native battery plant, a cross-repository database, or a deployed project approval service. Its visual scope explicitly states that no simulated plant is represented. [assets/svg-2.5d/scope.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/assets/svg-2.5d/scope.json#L1-L6) [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L15-L46)

## Confirmed local connections

| Connection | Implemented mechanism | Boundary |
|---|---|---|
| Templates/examples → Python auditors | Local Markdown parsing with explicit policy and date arguments | Only recognized selected records are evaluated |
| Status/deadline/completeness → readiness | Direct sibling-module calls | Separate specialized auditors remain separate |
| Source files → portfolio guide | Local source-path references and pinned URLs validated by `validate_guide.py` | A source link is not a runtime dependency |
| Lesson configuration → static page | Embedded JSON and JavaScript model evaluation | No Python audit execution in the browser |
| `docs` → Pages | GitHub Actions static artifact publication | Deployment provenance must be observed |
| README → handbook → source | Relative handbook navigation and immutable commit links | Human navigation, not automatic system integration |

Sources: [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L116-L240) [scripts/portfolio/validate_guide.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/portfolio/validate_guide.py#L1-L33) [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L338-L356) [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L54-L82).

No implemented runtime import, package dependency, API call, or data synchronization to another repository was established by the pinned source review. Portfolio branding, public repository links and source permalinks must not be labeled cross-repository integration.

## Public presentation dependency

The README overview image loads from the public owner profile repository at `mohammadrezwankhan/mohammadrezwankhan/main/assets/makeover/social/bess-qaqc-toolkit.png`. This is a confirmed presentation-asset dependency: its availability affects the README image, while the native auditors and embedded workload formulas do not depend on it. The image URL follows that repository’s `main` branch, so it is mutable. [Source README image](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/README.md#L3-L3).

## Portfolio navigation

The public [owner profile repository](https://github.com/mohammadrezwankhan/mohammadrezwankhan) is an appropriate navigation destination for a broader portfolio overview. This handbook does not assert that a particular profile-page update or portfolio deployment has already occurred. The repository's existing [portfolio guide](../portfolio/index.html) and [interactive lesson](../index.html) remain local entry points.

## Exportable concepts and boundaries

| Concept useful elsewhere | Representation here | Requirement before another system relies on it |
|---|---|---|
| Controlled evidence references | Check/evidence/instrument/document identifiers | Agree schemas, uniqueness scope and provenance ownership |
| Readiness outcome | Selected Boolean predicates and issue summaries | Preserve input manifest, policy, date and separate gate identities |
| JSON audit output | CLI-generated structures | Define versioning and compatibility; no existing stable API promise is inferred |
| Calendar semantics | ISO dates, signed due-day difference, inclusive calibration periods | Preserve timezone/date interpretation and assessment-date source |
| Synthetic workload quantities | Findings/minute, people, count, percentage | Retain fictional provenance and distinguish rates from accepted evidence |
| Source evidence | Commit permalink plus line range | Keep revision identity through copied or aggregated reports |

## Proposed future integration

A future portfolio dashboard could ingest deliberately published, sanitized audit summaries with repository SHA, input/policy fingerprints, assessment date, selected gates and limitations. That requires an approved schema and publication process. It is not implemented by the current static guide or this documentation package.

Do not combine this workload model's percentage with physical model outputs as a universal readiness or safety score. The same symbol can mean different things across the shared engine branches; use [parameters and symbols](../math-and-physics/PARAMETERS_AND_SYMBOLS.md) and preserve units and provenance when discussing other public projects.

## Owner decisions

Decide whether any machine-readable report becomes a supported portfolio contract, who owns sanitization and approval, and how source-to-deployment identity is retained. Until then, human-readable source links and the current repository-local workflows are the confirmed integration surface.
