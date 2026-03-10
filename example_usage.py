"""Example usage of blackboxml v0.5.0 — framework-agnostic experiment tracking."""

import random
from blackboxml import track, Run, MetricStore


# --- Example 1: @track decorator with MetricStore ---

@track(name="demo_model", tags=["example", "v1"])
def train_with_decorator():
    metrics = MetricStore()

    for epoch in range(5):
        metrics.reset()
        for batch in range(10):
            loss = 1.0 / (epoch + 1) + random.uniform(-0.05, 0.05)
            acc = 0.5 + epoch * 0.1 + random.uniform(-0.02, 0.02)
            metrics.update({"loss": loss, "acc": acc}, n=32)

        yield metrics.compute()


# --- Example 2: Run context manager ---

def train_with_context_manager():
    with Run(name="demo_manual", tags=["example", "manual"]) as run:
        for epoch in range(5):
            loss = 1.0 / (epoch + 1) + random.uniform(-0.05, 0.05)
            acc = 0.5 + epoch * 0.1 + random.uniform(-0.02, 0.02)
            run.log({"epoch": epoch, "loss": loss, "acc": acc})


if __name__ == "__main__":
    print("running @track example...")
    results = train_with_decorator()
    print(f"logged {len(results)} epochs\n")

    print("running Run context manager example...")
    train_with_context_manager()
    print("done\n")

    print("check blackboxml_logs/ for saved runs, or run: bbml runs")
