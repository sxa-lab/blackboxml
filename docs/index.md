# blackboxml

[![PyPI version](https://badge.fury.io/py/blackboxml.svg)](https://badge.fury.io/py/blackboxml)
[![Python Version](https://img.shields.io/pypi/pyversions/blackboxml.svg)](https://pypi.org/project/blackboxml)
[![Tests](https://github.com/sxa-lab/blackboxml/actions/workflows/test.yml/badge.svg)](https://github.com/sxa-lab/blackboxml/actions/workflows/test.yml)
[![Downloads](https://static.pepy.tech/badge/blackboxml)](https://pepy.tech/project/blackboxml)
[![ReadTheDocs](https://img.shields.io/readthedocs/blackboxml?label=ReadTheDocs)](https://blackboxml.readthedocs.io)

ML experiment tracking. Local, lightweight, framework-agnostic.

blackboxml logs your training runs as structured JSON. No accounts, no servers. It works with PyTorch, Keras, scikit-learn, or any Python training loop.

## Features

- **Three tracking modes.** `@track` decorator, `Run` context manager, or Keras `BlackBoxCallback`.
- **Automatic environment capture.** Git commit, dirty state, Python version, framework versions, hostname.
- **Batch-to-epoch aggregation.** `MetricStore` computes weighted averages across variable batch sizes.
- **Local JSON storage.** Runs saved to `blackboxml_logs/` as human-readable JSON, no database needed.
- **Built-in CLI.** List, inspect, and clean up runs from the terminal with `bbml`.
- **Visualisation.** Plot training and validation curves from any saved run.
- **Zero config.** Install and start logging in two lines of code.

## Install

```bash
pip install blackboxml
```

For Keras/TensorFlow callback support:

```bash
pip install blackboxml[keras]
```

Requires Python 3.10+.

## Quick start

### Decorator (generator functions)

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

### Context manager

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

### scikit-learn

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from blackboxml import Run

with Run(name="rf_search", tags=["sklearn"]) as run:
    for n in [50, 100, 200]:
        scores = cross_val_score(RandomForestClassifier(n_estimators=n), X, y, cv=5)
        run.log({"n_estimators": n, "accuracy": scores.mean()})
```

Each run is saved to `blackboxml_logs/<name>_<timestamp>/run.json`. Use `bbml runs` to list them, `bbml show <name>` to inspect one, or `visualise_run()` to plot the curves.

## Next steps

- [Usage guide](usage.md) covers every tracking mode and framework
- [CLI reference](cli.md) documents `bbml` commands and output format
- [What gets logged](logged.md) describes the full run schema and environment details
- [API reference](api.md) lists all class and function signatures
- [Visualisation](visualisation.md) explains how to plot training curves
