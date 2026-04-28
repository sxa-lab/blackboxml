# What gets logged

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
