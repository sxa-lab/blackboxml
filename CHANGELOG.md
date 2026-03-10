# Changelog

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/).

## [0.5.0] - 2026-03-11
### Framework-Agnostic Tracking

Broadens scope beyond Keras to support any ML framework. Builds on the original zero-friction logging idea with a cleaner, more portable architecture.

#### Added
- `@track` decorator for generator-based training functions (works with PyTorch, Keras, scikit-learn, or plain Python)
- `Run` context manager with explicit `.log()` calls for maximum flexibility
- `MetricStore` class for batch-level metric accumulation — eliminates the manual `running_loss` / `correct` / `total` boilerplate in PyTorch training loops
- `BlackBoxCallback` — proper Keras callback that captures per-epoch metrics, optimizer info, and model metadata
- `bbml` CLI with `runs`, `show`, and `clean` commands for inspecting logged experiments from the terminal
- Automatic environment capture: git commit hash, dirty status, Python version, framework versions, hostname
- Structured run output: each run gets its own directory with a `run.json` file
- Test suite with 25 tests covering store, metrics, and tracker modules

#### Changed
- Metric logging uses callbacks and context managers instead of patching `Model.fit()`
- `visualise_metrics()` replaced by `visualise_run()` for the new run.json format
- TensorFlow is now an optional extra (`pip install blackboxml[keras]`)
- Removed unused deps: `scikit-learn`, `numpy`, `pandas`. Added `click`.

---

## [0.2.0] - 2025-07-02
### Feature and Maintenance Update

#### Added
- Type hints and improved docstrings for all public APIs
- Python logging module (replaced print statements)
- Error handling in visualiser for graceful failure on malformed files

#### Changed
- Consistent `BlackBoxML` / `blackboxml` branding across all user-facing messages

---

## [0.1.0] - April 2025
### Initial Release

- First public release
- `autopilot()` for zero-setup Keras metric capture
- `Tracker` context manager for experiment tagging
- `visualise_metrics()` for plotting metric history
- Timestamped JSON logging to `blackboxml_logs/`
