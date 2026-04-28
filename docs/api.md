# API reference

Complete function and class signatures for all public APIs. For usage examples, see the [usage guide](usage.md).

The main package exports four objects:

```python
from blackboxml import track, Run, MetricStore, visualise_run
```

The Keras callback is imported separately to avoid loading TensorFlow:

```python
from blackboxml.callback import BlackBoxCallback
```

---

## track

```python
def track(
    name: str,
    tags: list[str] | None = None,
    log_dir: str = "blackboxml_logs"
) -> Callable
```

Decorator for generator functions. Each `yield` becomes a logged step.

**Parameters**

- **name:** run name, used in the directory and stored in JSON
- **tags:** optional list of tags (default: `None` → `[]`)
- **log_dir:** base directory for run storage (default: `"blackboxml_logs"`)

**Returns** a decorator. The decorated function returns `list[dict[str, float]]` containing all yielded metrics.

**Behaviour.** Creates a `Run` context internally, iterates the generator, logs each yielded dict, and saves on exit. If the function is not a generator, logs a warning and returns `[]`.

---

## Run

```python
class Run:
    def __init__(
        self,
        name: str,
        tags: list[str] | None = None,
        log_dir: str = "blackboxml_logs"
    ) -> None
```

Context manager for explicit metric logging.

**Parameters**

- **name:** run name
- **tags:** optional tags (default: `None` → `[]`)
- **log_dir:** base directory (default: `"blackboxml_logs"`)

### run.log

```python
def log(self, metrics: dict[str, float]) -> None
```

Append a metric dict as a new step.

### Context protocol

- `__enter__()` records start time (UTC) and captures environment. Returns `self`.
- `__exit__()` records end time, computes duration, and saves run as JSON. Does not suppress exceptions.

---

## MetricStore

```python
class MetricStore:
    def __init__(self) -> None
```

Accumulates batch-level metrics into epoch-level weighted averages.

### update

```python
def update(self, metrics: dict[str, float], n: int = 1) -> None
```

Add a batch of metrics weighted by `n` (batch size).

### compute

```python
def compute(self) -> dict[str, float]
```

Return weighted averages for all metrics since last reset.

**Raises** `ValueError` if called before any `update()`.

### reset

```python
def reset(self) -> None
```

Zero all accumulators. Call at the start of each epoch.

---

## visualise_run

```python
def visualise_run(
    run_path: str,
    save_path: str | None = None,
    show: bool = True
) -> None
```

Plot training metrics from a saved run.

**Parameters**

- **run_path:** path to a `run.json` file
- **save_path:** directory to save PNG plots (default: `None`, no files written)
- **show:** display plots interactively (default: `True`)

See [Visualisation](visualisation.md) for full details.

---

## BlackBoxCallback

```python
from blackboxml.callback import BlackBoxCallback

class BlackBoxCallback(keras.callbacks.Callback):
    def __init__(
        self,
        name: str,
        tags: list[str] | None = None,
        log_dir: str = "blackboxml_logs"
    ) -> None
```

Keras callback that logs per-epoch metrics and model metadata.

**Parameters**

- **name:** run name
- **tags:** optional tags (default: `None` → `[]`)
- **log_dir:** base directory (default: `"blackboxml_logs"`)

**Raises** `ImportError` if TensorFlow is not installed.

### Callback hooks

| Hook | What it does |
|------|-------------|
| `on_train_begin` | Records start time, captures model metadata (name, params, optimizer, learning rate) |
| `on_epoch_end` | Appends epoch metrics from Keras to the step list |
| `on_train_end` | Records end time, assembles run data, saves to disk |

---

## Store functions

Low-level persistence functions. You generally don't need these directly as they're called by `Run`, `@track`, and `BlackBoxCallback`.

### save_run

```python
def save_run(run_data: dict, base_dir: str = "blackboxml_logs") -> str
```

Write run data to `<base_dir>/<name>_<timestamp>/run.json`. Returns the file path.

### load_run

```python
def load_run(run_path: str) -> dict
```

Read and parse a `run.json` file. Raises `FileNotFoundError` or `json.JSONDecodeError` on failure.

### list_runs

```python
def list_runs(base_dir: str = "blackboxml_logs") -> list[dict]
```

Scan a directory for runs. Returns a list of run dicts sorted newest-first. Skips unreadable files with a warning.

### delete_all_runs

```python
def delete_all_runs(base_dir: str = "blackboxml_logs") -> int
```

Delete the entire log directory. Returns the number of run directories removed. This is destructive and cannot be undone.
