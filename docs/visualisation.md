# Visualisation

blackboxml plots training and validation curves from saved runs using matplotlib.

## Basic usage

```python
from blackboxml import visualise_run

visualise_run("blackboxml_logs/resnet_cifar10_20260310_142201/run.json")
```

This opens an interactive matplotlib window with one plot per metric. Training and validation curves (e.g. `loss` and `val_loss`) are shown on the same axes.

## Saving plots

Pass `save_path` to write PNG files instead of (or alongside) displaying them:

```python
# Save to disk, don't display
visualise_run(
    "blackboxml_logs/resnet_cifar10_20260310_142201/run.json",
    save_path="plots/",
    show=False
)
```

This creates one PNG per metric:

```
plots/
├── loss_vs_epochs.png
├── acc_vs_epochs.png
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `run_path` | `str` | required | Path to a `run.json` file. |
| `save_path` | `str \| None` | `None` | Directory to save PNG plots. Created if it doesn't exist. |
| `show` | `bool` | `True` | Display plots interactively via `plt.show()`. |

## How plots are generated

1. **Load** the run from `run_path`.
2. **Collect** all unique metric keys across steps, excluding `epoch`.
3. **Determine x-axis.** Uses explicit `epoch` values if present, otherwise step indices (0, 1, 2, ...).
4. **Plot** each primary metric (non-`val_` prefixed) on its own figure. If a matching `val_` metric exists (e.g. `val_loss` for `loss`), both are plotted on the same axes.
5. **Save** and/or **display** based on parameters.

Each plot includes a title in the format `{metric} vs Epochs, {run_name}`, with axis labels, legend, and grid.

## Finding the run path

Run directories follow the pattern `blackboxml_logs/<name>_<YYYYMMDD_HHMMSS>/run.json`. You can list available runs with `bbml runs`, then construct the path:

```python
visualise_run("blackboxml_logs/resnet_cifar10_20260310_142201/run.json",
              save_path="plots/")
```

Or find it programmatically:

```python
from blackboxml.store import list_runs

runs = list_runs()
latest = runs[0]  # sorted newest-first
# Use the run data directly, or locate the file on disk
```

## Error handling

- **File not found.** Logs an error and returns, no exception raised.
- **Invalid JSON.** Logs an error and returns.
- **No steps.** Logs a warning and returns.
- **Plotting error on one metric.** Logs the exception and continues to the next metric.
