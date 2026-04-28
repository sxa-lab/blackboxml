# Usage

blackboxml provides three tracking modes: a **decorator** for generator-based loops, a **context manager** for imperative logging, and a **Keras callback** for `model.fit()`. All three produce the same JSON output. This page covers each mode and shows how to use them with PyTorch, Keras, scikit-learn, and plain Python.

## @track decorator

The `@track` decorator wraps a generator function. Each `yield` becomes a logged step.

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

results = train()
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Name for the run. Used in the directory name and stored in the JSON. |
| `tags` | `list[str] \| None` | `None` | Tags to associate with the run. Useful for filtering runs later. |
| `log_dir` | `str` | `"blackboxml_logs"` | Base directory for saving run data. |

### How it works

1. Calls your function to get a generator.
2. Opens a `Run` context manager internally.
3. Iterates over yielded dicts, logging each one as a step.
4. On exit, saves the full run to disk.
5. Returns a list of all yielded metric dicts.

If the decorated function is not a generator (doesn't `yield`), blackboxml logs a warning and returns an empty list.

### Yielded values

Each yielded value should be a `dict[str, float]`. Common patterns:

```python
# Simple - yield a dict directly
yield {"loss": 0.42, "acc": 0.91}

# With MetricStore - yield weighted epoch averages
yield metrics.compute()

# With validation - yield both in one dict
yield {"train_loss": t_loss, "val_loss": v_loss, "val_acc": v_acc}
```

## Run context manager

For more control, use `Run` directly. Call `run.log()` each time you have metrics to record.

```python
from blackboxml import Run

with Run(name="resnet_cifar10", tags=["pytorch"]) as run:
    for epoch in range(10):
        loss = train_one_epoch()
        val_loss = validate()
        run.log({"loss": loss, "val_loss": val_loss, "epoch": epoch})
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Run name. |
| `tags` | `list[str] \| None` | `None` | Optional tags. |
| `log_dir` | `str` | `"blackboxml_logs"` | Base directory for logs. |

### Methods

#### `run.log(metrics: dict[str, float]) -> None`

Appends a metric dict as a new step. Call once per epoch or at whatever granularity you want.

```python
run.log({"loss": 0.42, "acc": 0.91})
run.log({"loss": 0.38, "acc": 0.93})
```

### Lifecycle

- **`__enter__`** records start time and captures environment metadata (git, Python, frameworks, hostname).
- **`__exit__`** records end time, computes duration, and saves the run as JSON.
- Exceptions are **not** suppressed. If your training code raises, the context manager exits cleanly and re-raises.

## MetricStore

`MetricStore` accumulates batch-level metrics into epoch-level weighted averages. It's pure Python with no framework dependencies.

```python
from blackboxml import MetricStore

metrics = MetricStore()

for epoch in range(10):
    metrics.reset()
    for batch in dataloader:
        loss, acc = train_step(batch)
        metrics.update({"loss": loss, "acc": acc}, n=len(batch))

    epoch_avg = metrics.compute()
    # {"loss": 0.42, "acc": 0.91}  - weighted by batch size
```

### Methods

#### `update(metrics: dict[str, float], n: int = 1) -> None`

Accumulate a batch of metrics weighted by batch size `n`.

```python
# Each call adds value * n to the running weighted sum
metrics.update({"loss": 0.5, "acc": 0.8}, n=32)
metrics.update({"loss": 0.4, "acc": 0.9}, n=32)
```

The `n` parameter matters when batch sizes vary (e.g. the last batch in an epoch is smaller). Without it, small batches would be overweighted.

#### `compute() -> dict[str, float]`

Returns the weighted average for each metric since the last reset.

Raises `ValueError` if called before any `update()` call.

#### `reset() -> None`

Zeros all accumulators. Call at the start of each epoch.

### Typical pattern

```python
metrics = MetricStore()
for epoch in range(num_epochs):
    metrics.reset()                          # clear for this epoch
    for batch in dataloader:
        loss = train_step(batch)
        metrics.update({"loss": loss}, n=len(batch))  # accumulate
    yield metrics.compute()                  # epoch average
```

## Keras callback

`BlackBoxCallback` plugs into `model.fit()` and logs per-epoch metrics automatically.

```python
from blackboxml.callback import BlackBoxCallback

callback = BlackBoxCallback(
    name="lstm_nlp",
    tags=["keras", "nlp"],
    log_dir="blackboxml_logs"
)

model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=10,
    callbacks=[callback]
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Run name. |
| `tags` | `list[str] \| None` | `None` | Optional tags. |
| `log_dir` | `str` | `"blackboxml_logs"` | Base directory for logs. |

### What it captures

- **Per-epoch metrics** including loss, accuracy, val_loss, val_accuracy, and any custom metrics from `model.compile()`
- **Model metadata** including model name, parameter count, optimizer name, and learning rate
- **Environment** including Python version and TensorFlow version
- **Timing** including start time, end time, and duration

### Requirements

Requires TensorFlow. Install with:

```bash
pip install blackboxml[keras]
```

Raises `ImportError` at instantiation if TensorFlow is not installed.

## scikit-learn

scikit-learn doesn't have an epoch-based training loop, but you can log cross-validation scores, grid search results, or any per-configuration metrics. Use the `Run` context manager:

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from blackboxml import Run

with Run(name="rf_grid_search", tags=["sklearn", "random-forest"]) as run:
    for n_trees in [50, 100, 200, 500]:
        clf = RandomForestClassifier(n_estimators=n_trees)
        scores = cross_val_score(clf, X, y, cv=5, scoring="accuracy")
        run.log({
            "n_estimators": n_trees,
            "mean_accuracy": scores.mean(),
            "std_accuracy": scores.std()
        })
```

Or use `@track` with a generator to log each configuration as a step:

```python
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from blackboxml import track

@track(name="svm_kernel_search", tags=["sklearn", "svm"])
def search():
    for kernel in ["linear", "rbf", "poly"]:
        clf = SVC(kernel=kernel)
        scores = cross_val_score(clf, X, y, cv=5)
        yield {"kernel_acc": scores.mean()}

search()
```

## Plain Python

blackboxml has no framework dependencies for core tracking. A hand-written gradient descent loop works the same way:

```python
from blackboxml import Run

with Run(name="gradient_descent", tags=["scratch"]) as run:
    w = 0.0
    for step in range(100):
        grad = compute_gradient(w)
        w -= 0.01 * grad
        if step % 10 == 0:
            run.log({"step": step, "loss": compute_loss(w), "weight": w})
```

## Custom log directory

All three tracking modes accept a `log_dir` parameter:

```python
@track(name="my_run", log_dir="/data/experiments")
def train(): ...

with Run(name="my_run", log_dir="/data/experiments") as run: ...

BlackBoxCallback(name="my_run", log_dir="/data/experiments")
```

Runs are saved to `<log_dir>/<name>_<timestamp>/run.json`.
