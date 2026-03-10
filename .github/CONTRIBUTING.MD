# Contributing to BlackBoxML

Contributions are welcome — bug fixes, docs improvements, new features.

## Setup

```bash
git clone https://github.com/stuartasiimwe7/blackboxml.git
cd blackboxml
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install pytest
```

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
