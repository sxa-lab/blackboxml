# Contributing

Bug reports, feature requests, and pull requests are welcome.

## Getting started

```bash
git clone https://github.com/sxa-lab/blackboxml.git
cd blackboxml
pip install -e .
```

For Keras callback development:

```bash
pip install -e ".[keras]"
```

## Running tests

```bash
pytest
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

## Code style

- Follow PEP 8
- Use Python's `logging` module
- Type hints on all public APIs

## Templates

- [Bug reports](https://github.com/sxa-lab/blackboxml/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature requests](https://github.com/sxa-lab/blackboxml/blob/main/.github/ISSUE_TEMPLATE/feature_request.md)
- [Security policy](https://github.com/sxa-lab/blackboxml/blob/main/.github/SECURITY.MD)
- [Code of conduct](https://github.com/sxa-lab/blackboxml/blob/main/.github/CODE_OF_CONDUCT.MD)

## License

[Apache License 2.0](https://github.com/sxa-lab/blackboxml/blob/main/LICENSE), maintained by [SxA Lab](https://github.com/sxa-lab)
