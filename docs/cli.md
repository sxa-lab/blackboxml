# CLI

blackboxml includes a command-line tool called `bbml` for inspecting and managing logged runs.

## bbml runs

List all logged training runs.

```
$ bbml runs
NAME              DATE                 DURATION  STEPS  TAGS
----------------------------------------------------------------
resnet_cifar10    2026-03-10 14:22:01    13m 46s     10  pytorch, cifar10
lstm_nlp          2026-03-10 11:05:33     4m 12s      5  keras
svm_baseline      2026-03-09 09:15:00        45s      1  sklearn
```

Runs are sorted newest-first by start time. The table columns are:

| Column | Description |
|--------|-------------|
| NAME | Run name as passed to `@track`, `Run`, or `BlackBoxCallback` |
| DATE | Start time formatted as `YYYY-MM-DD HH:MM:SS` |
| DURATION | Human-readable duration: `45s`, `4m 12s`, or `2h 5m 30s` |
| STEPS | Number of logged steps (epochs) |
| TAGS | Comma-separated tag list |

If no runs exist, prints `no runs found.`

Missing or unreadable fields display as `-`.

## bbml show

Pretty-print a single run by name.

```
$ bbml show resnet_cifar10
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
  "start": "2026-03-10T14:22:01.123456",
  "end": "2026-03-10T14:35:47.654321",
  "duration_seconds": 826.53,
  "steps": [
    {"loss": 0.842, "acc": 0.65},
    {"loss": 0.671, "acc": 0.78}
  ]
}
```

Output is formatted JSON with 2-space indent. If no matching run exists, prints `run not found: <name>`.

## bbml clean

Delete all logged runs.

```
$ bbml clean
delete all runs? [y/N]: y
deleted 3 run(s).
```

Prompts for confirmation before deleting. Defaults to No if you press Enter without typing. This removes the entire `blackboxml_logs/` directory and cannot be undone.

## Where runs are stored

By default, runs are saved to `blackboxml_logs/` in the current working directory. Each run gets its own subdirectory:

```
blackboxml_logs/
├── resnet_cifar10_20260310_142201/
│   └── run.json
├── lstm_nlp_20260310_110533/
│   └── run.json
└── svm_baseline_20260309_091500/
    └── run.json
```

The directory name is `<sanitized_name>_<YYYYMMDD_HHMMSS>`. Non-alphanumeric characters in run names (except dashes and underscores) are replaced with underscores.
