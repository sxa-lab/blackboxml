# Contributing to BlackBoxML

Bug reports, feature requests, and pull requests are welcome.

## Setup

```bash
git clone https://github.com/sxa-lab/blackboxml.git
cd blackboxml
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install pytest
```

For Keras callback development:

```bash
pip install -e ".[keras]"
```

## Running tests

```bash
pytest tests/ -v
```

## Building the package

```bash
python setup.py sdist bdist_wheel
```

## Project structure

| File | Role |
|------|------|
| `__init__.py` | Public exports |
| `tracker.py` | `@track` decorator and `Run` context manager |
| `metrics.py` | `MetricStore` batch-to-epoch aggregation |
| `store.py` | JSON persistence (`save_run`, `load_run`, `list_runs`, `delete_all_runs`) |
| `callback.py` | `BlackBoxCallback` for Keras |
| `visualiser.py` | `visualise_run()` plotting |
| `cli.py` | `bbml` CLI built with Click |

## Workflow

1. Fork the repo and create a branch (`fix/logger-bug`, `feat/compare-runs`)
2. Make your changes. Follow PEP 8, add type hints to public APIs.
3. Run tests: `pytest tests/ -v`
4. Commit with a clear message, push, and open a PR against `main`

## Guidelines

- Check existing issues before opening a new one
- Open an issue first for major changes
- Include tests for new functionality
- Use the [pull request template](./PULL_REQUEST_TEMPLATE.MD)

## Reporting bugs

Use the [bug report template](./ISSUE_TEMPLATE/bug_report.md). Include your Python version, blackboxml version, and steps to reproduce.

## License

By contributing, you agree your work will be licensed under the same [Apache 2.0 license](../LICENSE) as the project.
