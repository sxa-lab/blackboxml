[![PyPI version](https://badge.fury.io/py/blackboxml.svg)](https://badge.fury.io/py/blackboxml) [![Python Version](https://img.shields.io/pypi/pyversions/blackboxml.svg)](https://pypi.org/project/blackboxml/) [![Tests](https://github.com/sxa-lab/blackboxml/actions/workflows/test.yml/badge.svg)](https://github.com/sxa-lab/blackboxml/actions/workflows/test.yml) [![Downloads](https://static.pepy.tech/badge/blackboxml)](https://pepy.tech/project/blackboxml)

# blackboxml

ML experiment tracking. Local, lightweight, framework-agnostic.

Works with PyTorch, Keras, scikit-learn, or plain Python.

## Install

```bash
pip install blackboxml
pip install blackboxml[keras]  # optional TensorFlow support
```

## Usage

### `@track` decorator

```python
from blackboxml import track, MetricStore

@track(name="resnet_cifar10", tags=["pytorch", "cifar10"])
def train():
    metrics = MetricStore()
    for epoch in range(10):
        metrics.reset()
        for batch in dataloader:
            loss, acc = train_step(batch)
            metrics.update({"loss": loss, "acc": acc}, n=len(batch))
        yield metrics.compute()

train()
```

### `Run` context manager

```python
from blackboxml import Run

with Run(name="resnet_cifar10", tags=["pytorch"]) as run:
    for epoch in range(10):
        run.log({"loss": train_one_epoch(), "epoch": epoch})
```

### Keras callback

```python
from blackboxml.callback import BlackBoxCallback

model.fit(x_train, y_train, epochs=10,
          callbacks=[BlackBoxCallback(name="lstm_nlp", tags=["keras"])])
```

## CLI

```
$ bbml runs
NAME              DATE                 DURATION  STEPS  TAGS
----------------------------------------------------------------
resnet_cifar10    2026-03-10 14:22:01    13m 46s     10  pytorch, cifar10
lstm_nlp          2026-03-10 11:05:33     4m 12s      5  keras

$ bbml show resnet_cifar10
$ bbml clean
```

## What gets logged

Each run saves to `blackboxml_logs/<name>_<timestamp>/run.json`:

```json
{
  "name": "resnet_cifar10",
  "tags": ["pytorch", "cifar10"],
  "environment": {
    "git_commit": "a3f91bc",
    "git_dirty": false,
    "python": "3.11.2",
    "torch": "2.3.0",
    "hostname": "lab-gpu-01"
  },
  "start": "2026-03-10T14:22:01",
  "end": "2026-03-10T14:35:47",
  "duration_seconds": 826,
  "steps": [
    {"loss": 0.842, "acc": 0.65},
    {"loss": 0.671, "acc": 0.78}
  ]
}
```

Git commit, Python version, framework versions, and hostname are captured automatically.

## Releases

| Version | Date | What changed |
|---------|------|-------------|
| [0.1.0](https://pypi.org/project/blackboxml/0.1.0/) | Apr 2025 | Initial release — Keras auto-logging, `visualise_metrics` |
| [0.2.0](https://pypi.org/project/blackboxml/0.2.0/) | Jul 2025 | Type hints, logging module, error handling |
| **0.5.0** | Mar 2026 | Framework-agnostic rewrite — `@track`, `Run`, `MetricStore`, `bbml` CLI |

## Contributing

See [Contributing Guidelines](./.github/CONTRIBUTING.MD) to get started. Bug reports, feature requests, and pull requests are welcome.

- [Bug reports](./.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature requests](./.github/ISSUE_TEMPLATE/feature_request.md)
- [Security policy](./.github/SECURITY.MD)
- [Code of conduct](./.github/CODE_OF_CONDUCT.MD)

## License

[Apache License 2.0](./LICENSE)

## Maintainer

Maintained by [SxA Lab](https://github.com/sxa-lab)
