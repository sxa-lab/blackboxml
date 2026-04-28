# What gets logged

Every run is saved as a JSON file at `blackboxml_logs/<name>_<timestamp>/run.json`. This page documents the full schema.

## Run schema

```json
{
  "name": "resnet_cifar10",
  "tags": ["pytorch", "cifar10"],
  "environment": {
    "git_commit": "a3f91bc",
    "git_dirty": false,
    "python": "3.11.2",
    "torch": "2.3.0",
    "tensorflow": null,
    "hostname": "lab-gpu-01"
  },
  "start": "2026-03-10T14:22:01.123456",
  "end": "2026-03-10T14:35:47.654321",
  "duration_seconds": 826.53,
  "steps": [
    {"loss": 0.842, "acc": 0.65},
    {"loss": 0.671, "acc": 0.78},
    {"loss": 0.534, "acc": 0.85}
  ]
}
```

## Fields

### Top-level

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Run name as passed to `@track`, `Run`, or `BlackBoxCallback`. |
| `tags` | `string[]` | Tags associated with the run. Empty list if none provided. |
| `environment` | `object` | Automatically captured environment metadata. |
| `start` | `string` | ISO 8601 timestamp when the run started (UTC). |
| `end` | `string` | ISO 8601 timestamp when the run finished (UTC). |
| `duration_seconds` | `float` | Wall-clock duration in seconds. |
| `steps` | `object[]` | List of metric dicts, one per logged step (typically one per epoch). |

### Environment

Captured automatically when the run starts. No configuration needed.

| Field | Type | Description |
|-------|------|-------------|
| `git_commit` | `string \| null` | Short hash of the current git commit. `null` if not in a git repo. |
| `git_dirty` | `bool \| null` | `true` if there are uncommitted changes. `null` if git is unavailable. |
| `python` | `string` | Python version (e.g. `"3.11.2"`). |
| `torch` | `string \| null` | PyTorch version if installed, otherwise `null`. |
| `tensorflow` | `string \| null` | TensorFlow version if installed, otherwise `null`. |
| `hostname` | `string` | Machine hostname. |

### Steps

Each entry in `steps` is a flat dict of metric names to float values. The structure depends on what you log:

With `@track` or `Run`, each step contains whatever you yield or log:

```json
{"loss": 0.42, "acc": 0.91}
```

With `BlackBoxCallback`, Keras passes its own metric names plus the epoch index:

```json
{"epoch": 0, "loss": 0.42, "accuracy": 0.91, "val_loss": 0.45, "val_accuracy": 0.89}
```

There is no fixed set of metric names, blackboxml stores whatever keys you provide.

### Model metadata (Keras only)

When using `BlackBoxCallback`, the run also includes a `model` field:

```json
{
  "model": {
    "name": "sequential",
    "params": 1250410,
    "optimizer": "Adam",
    "learning_rate": 0.001
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `model.name` | `string` | Keras model name. |
| `model.params` | `int` | Total trainable + non-trainable parameters. |
| `model.optimizer` | `string` | Optimizer class name. |
| `model.learning_rate` | `float \| null` | Initial learning rate. `null` if extraction fails. |

## File structure

```
blackboxml_logs/
├── resnet_cifar10_20260310_142201/
│   └── run.json
└── lstm_nlp_20260310_110533/
    └── run.json
```

- Directory name: `<sanitized_name>_<YYYYMMDD_HHMMSS>`
- Name sanitisation: characters outside `[a-zA-Z0-9_-]` are replaced with `_`
- JSON is pretty-printed with 2-space indent
- Timestamps use ISO 8601 format with microseconds

## Comparing runs

Since runs are plain JSON files, you can compare them with standard tools:

```bash
# diff two runs
diff <(jq .steps run1/run.json) <(jq .steps run2/run.json)

# extract a metric across all runs
for f in blackboxml_logs/*/run.json; do
    jq '{name: .name, final_loss: .steps[-1].loss}' "$f"
done
```

Or use `bbml show <name>` to inspect a run from the terminal, and `visualise_run()` to plot the training curves.
