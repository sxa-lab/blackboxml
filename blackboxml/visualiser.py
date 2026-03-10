"""Single-run metric visualisation for BlackBoxML."""

import logging
import os

import matplotlib.pyplot as plt

from blackboxml.store import load_run

logger = logging.getLogger("blackboxml")


def visualise_run(
    run_path: str,
    save_path: str | None = None,
    show: bool = True,
) -> None:
    """Plot training metrics for a single run.

    Each metric (and its ``val_`` counterpart, when present) is rendered on
    its own figure with epochs on the x-axis.

    Args:
        run_path: Path to a ``run.json`` file produced by the store module.
        save_path: Directory in which to save plots as PNG files.  When
            *None*, plots are not written to disk.
        show: If *True*, display each figure interactively via
            ``plt.show()``.  If *False*, close figures after optional saving.
    """
    try:
        run_data = load_run(run_path)
    except FileNotFoundError:
        logger.error("Run file not found: %s", run_path)
        return
    except ValueError:
        logger.error("Run file is not valid JSON: %s", run_path)
        return

    steps: list[dict] = run_data.get("steps", [])
    if not steps:
        logger.warning("No steps found in run: %s", run_path)
        return

    run_name: str = run_data.get("name", "unnamed")

    # Collect every metric key present across all steps (excluding "epoch").
    all_keys: set[str] = set()
    for step in steps:
        all_keys.update(step.keys())
    all_keys.discard("epoch")

    if not all_keys:
        logger.warning("No metric keys found in steps for run: %s", run_path)
        return

    # Build the x-axis from explicit epoch values or fall back to indices.
    if "epoch" in steps[0]:
        x_values: list[int | float] = [step["epoch"] for step in steps]
    else:
        x_values = list(range(len(steps)))

    if save_path is not None:
        os.makedirs(save_path, exist_ok=True)

    # Determine which keys to iterate: skip val_ keys (they are paired with
    # their training counterpart automatically).
    primary_keys = sorted(k for k in all_keys if not k.startswith("val_"))

    for metric in primary_keys:
        val_metric = f"val_{metric}"
        has_val = val_metric in all_keys

        try:
            y_train = [step.get(metric) for step in steps]

            fig, ax = plt.subplots()
            ax.plot(x_values, y_train, label=metric)

            if has_val:
                y_val = [step.get(val_metric) for step in steps]
                ax.plot(x_values, y_val, label=val_metric)

            ax.set_xlabel("Epochs")
            ax.set_ylabel(metric)
            ax.set_title(f"{metric} vs Epochs \u2014 {run_name}")
            ax.legend()
            ax.grid(True)

            if save_path is not None:
                filename = os.path.join(save_path, f"{metric}_vs_epochs.png")
                fig.savefig(filename)
                logger.info("Saved plot: %s", filename)

            if show:
                plt.show()
            else:
                plt.close(fig)

        except Exception:
            logger.exception("Error plotting metric '%s' for run: %s", metric, run_path)
            plt.close("all")
