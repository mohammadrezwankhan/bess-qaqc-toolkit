# Setup and reproducibility

[Handbook index](../INDEX.md)

## Runtime contract

The documented and CI-selected runtime is **Python 3.12**. On 2026-11-19 the authoring environment ran the existing suite on **CPython 3.12.14 on Linux**: 180 tests passed. That observation does not establish support for every OS or Python release. No `requirements.txt`, Python package manifest or third-party native runtime dependency is present in the pinned tree; the native scripts import the standard library and sibling modules. [README.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/README.md#L59-L71) [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L39-L54) [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L1-L60)

## Acquire the audited implementation

```bash
git clone https://github.com/mohammadrezwankhan/bess-qaqc-toolkit.git
cd bess-qaqc-toolkit
git checkout --detach af44c932684dfd120dea05d150cefcc3e47539a0
python3.12 -m venv ../bess-qaqc-venv
. ../bess-qaqc-venv/bin/activate
python --version
```

The detached checkout reproduces the implementation referenced by this handbook. Keep new work on a separate branch/check-out. The environment is deliberately placed beside the repository because the existing ignore rules do not exclude a `.venv/` directory. No dependency installation is needed for the native checks. [.gitignore](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.gitignore#L1-L14)

On Windows, the analogous environment commands are `py -3.12 -m venv ..\bess-qaqc-venv` and `..\bess-qaqc-venv\Scripts\Activate.ps1`; that shell recipe was not executed in this Linux observation.

## Run from the repository root

```bash
python -m unittest discover -s tests -v
python scripts/validate_templates.py --strict-governance
python scripts/audit_completeness.py templates \
  --policy config/readiness-completeness-policy.example.json
python scripts/audit_readiness.py examples/readiness-gate-passing-record.md \
  --status-policy config/readiness-status-policy.example.json \
  --completeness-policy config/readiness-completeness-policy.example.json \
  --as-of 2026-07-21 --require-source-coverage
```

These are existing CI commands, with the report printed rather than written to runner-temporary storage. The fixed date belongs to the fixture. Changing it changes the question being evaluated and may correctly change the result. [.github/workflows/markdown-maintenance.yml](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/.github/workflows/markdown-maintenance.yml#L45-L69)

Use the [worked examples](WORKED_EXAMPLES_AND_LABS.md) for the other audit families. A passing readiness example does not run every family. For a real controlled record set, record which audits apply and why each excluded audit does not apply.

## Preserve an evidence bundle

Retain the Git revision, Python version, exact arguments, working directory, input file hashes, policy file hashes, explicit evaluation date, stdout, stderr and exit code. Use a report directory outside the scanned inputs:

```bash
mkdir -p ../bess-audit-output
python scripts/audit_readiness.py examples/readiness-gate-passing-record.md \
  --status-policy config/readiness-status-policy.example.json \
  --completeness-policy config/readiness-completeness-policy.example.json \
  --as-of 2026-07-21 --require-source-coverage \
  --format json --output ../bess-audit-output/readiness.json
```

`--output` creates parent directories and writes the destination; it is not restricted by the input-path boundary. Choose a destination that will not replace a record, policy or other evidence. [scripts/audit_readiness.py](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/scripts/audit_readiness.py#L460-L506)

For private project records, use controlled storage approved for that project. The public example files contain fabricated identifiers and do not include the referenced controlled documents. [examples/lifecycle-worked-example.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/lifecycle-worked-example.md#L5-L11) [examples/punch-list-closeout-passing.md](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/examples/punch-list-closeout-passing.md#L13-L14)

## Browser lessons

Open `docs/index.html` directly in a browser for the self-contained workload computation. Source links need network access; the Python audit commands are not executed by the page. Alternatively run `python -m http.server 8000 --directory docs` from the repository root and open `http://localhost:8000/`. The local HTTP server is an optional viewing recipe, not a production hosting recommendation.

The source-linked guide uses browser local storage for notes/progress when available and offers export when storage is unavailable. Clearing browser data can remove those notes. [docs/portfolio/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/portfolio/index.html#L285-L290) [docs/portfolio/index.html](https://github.com/mohammadrezwankhan/bess-qaqc-toolkit/blob/af44c932684dfd120dea05d150cefcc3e47539a0/docs/portfolio/index.html#L304-L307)

The browser model, configuration schema and fixture tolerances are documented in [math and limits](../math-and-physics/EQUATIONS_AND_DERIVATIONS.md). A current-browser interactive run was not part of the Python test-suite observation.
