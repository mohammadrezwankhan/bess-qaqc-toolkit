# Toolchain and dependency matrix

[Handbook](../INDEX.md) · [Setup](../developer/SETUP_AND_REPRODUCIBILITY.md) · [Release playbook](CI_CD_AND_RELEASE_PLAYBOOK.md)

## Runtime and review capabilities

| Component | Declared / configured capability | Observed or inspected state | Limit |
|---|---|---|---|
| Native Python CLIs | Python 3.12 in GitHub Actions | CPython 3.12.14 ran the 180-test source baseline and native examples locally | No supported-version range or multi-version matrix is declared |
| Python dependencies | Standard library and sibling script modules | No requirements, pyproject, setup, Pipfile, or conda environment in the pinned tree | Do not infer compatibility with untested Python versions |
| Unit framework | `unittest` discovery | Existing 12 test files inspected; 180 tests executed | No measured coverage percentage |
| Browser lesson | Static HTML/CSS/JavaScript and embedded JSON | Engine formulas and configuration inspected | No formal browser support table or complete interactive-browser test is asserted |
| Portfolio guide | Static HTML, JSON, SVG and localStorage preference handling | Existing Python validator passed | Validator does not replace accessibility or interaction testing |
| GitHub Pages | Upload and serve `docs` via Actions | Workflow inspected and existing route observed | Candidate deployment requires its own evidence |
| Git | Source/history transport | Immutable source, tree and blob identities verified | No implication that the authored candidate was pushed |
| Markdown/CFF review tools | Operational documentation checks | Separate reviewer environment | They are not new repository runtime dependencies |

Python declaration: [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L39-L49). Browser implementation: [docs/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/index.html#L150-L336). Portfolio validator: [scripts/portfolio/validate_guide.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/portfolio/validate_guide.py#L1-L33).

Native imports include `argparse`, `collections`, `dataclasses`, `datetime`, `json`, `pathlib`, `re`, and `sys`. These inspected scripts do not require MATLAB, NumPy, SciPy, a database, a GPU, an API key, or an installation step for an application package. This describes dependencies, not interoperability or untested-version support. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L1-L66) [scripts/audit_calibration_traceability.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_calibration_traceability.py#L1-L49)

## Pinned Actions

These are the executable pins in source revision `af44c932684dfd120dea05d150cefcc3e47539a0`; version labels are comments present in the workflow.

| Action | Commit pin | Source comment |
|---|---|---|
| `actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | v7.0.1 |
| `actions/setup-python` | `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0` | v7.1.0 |
| `lycheeverse/lychee-action` | `e7477775783ea5526144ba13e8db5eec57747ce8` | v2 |
| `actions/configure-pages` | `45bfe0192ca1faeb007ade9deae92b16b8254a0d` | v6.0.0 |
| `actions/upload-pages-artifact` | `fc324d3547104276b827a68afc52ff2a11cc49c9` | v5.0.0 |
| `actions/deploy-pages` | `368f82528645a54fb793d4d04e342629a3f51346` | v5.0.1 |

Sources: [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L34-L104) [.github/workflows/deploy-dashboard.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/deploy-dashboard.yml#L25-L82). Dependabot is configured for weekly GitHub Actions updates with at most five open pull requests. It is not configured as a Python dependency updater here. [.github/dependabot.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/dependabot.yml#L1-L7)

## Data, examples, and provenance

| Material | Provenance and use | Rights / control boundary |
|---|---|---|
| Markdown templates | Project-neutral repository material | Preserve the repository license; separately control project records inserted by users |
| Passing/failing fixtures | Controlled examples and test inputs | Demonstrate software behavior, not real project acceptance |
| Active lesson inputs | Explicitly fictional, uncalibrated presets | Do not relabel as measured staffing data |
| Generic engine constants | Literal simplified coefficients in JavaScript | No cited field calibration or equipment-qualification dataset |
| SVG/CSS assets | Tracked presentation and instructional assets | Preserved; XML/geometry inspection is not scientific validation |
| Real certificates, signatures, drawings, or measurements | Not supplied as a verified field dataset by this toolkit | Require lawful access and project confidentiality; do not add them to public examples casually |

Declarations: [LICENSE](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/LICENSE#L1-L21) [CITATION.cff](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/CITATION.cff#L1-L16). Teaching calibration label: [docs/lesson-config.json](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/lesson-config.json#L54-L144). Existing confidentiality rule: [CONTRIBUTING.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/CONTRIBUTING.md#L12-L20).

No separate third-party measurement dataset license was identified among tracked inputs. This does not grant rights to certificates, OEM instructions, standards, or project data later supplied by a user. CFF metadata contains no DOI or software version at the pinned revision; preserve known metadata rather than filling those fields speculatively.

## Offline and environment boundaries

The native scripts operate on local files and can run without network services once source and a compatible Python interpreter are available. The static lesson embeds its formulas; external source links and repository updates require connectivity. Portfolio preference persistence depends on localStorage availability. No claim is made that every hosted asset, external link, or browser security policy has been exercised offline. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506) [docs/portfolio/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/portfolio/index.html#L285-L290)

Use an isolated environment outside the checkout and a separate report directory. Preserve exact policies and assessment dates with audit outputs. See the [setup guide](../developer/SETUP_AND_REPRODUCIBILITY.md).
