import datetime
import platform
import logging
from typing import Optional

logger = logging.getLogger("blackboxml")

try:
    import tensorflow as tf
    from tensorflow import keras
    HAS_TF = True
except ImportError:
    HAS_TF = False


class BlackBoxCallback(keras.callbacks.Callback if HAS_TF else object):
    """Keras callback that logs per-epoch metrics and run metadata to disk."""

    def __init__(
        self,
        name: str,
        tags: Optional[list[str]] = None,
        log_dir: str = "blackboxml_logs",
    ) -> None:
        if not HAS_TF:
            raise ImportError(
                "BlackBoxCallback requires tensorflow. "
                "Install it with: pip install blackboxml[keras]"
            )
        super().__init__()
        self.name = name
        self.tags = tags or []
        self.log_dir = log_dir
        self._steps: list[dict] = []
        self._start_time: Optional[datetime.datetime] = None
        self._model_info: dict = {}

    def on_train_begin(self, logs: Optional[dict] = None) -> None:
        self._start_time = datetime.datetime.now()
        self._steps = []

        model_name = self.model.name
        total_params = self.model.count_params()

        optimizer = self.model.optimizer
        optimizer_name = type(optimizer).__name__
        try:
            lr_value = float(optimizer.learning_rate)
        except Exception:
            lr_value = None

        self._model_info = {
            "name": model_name,
            "params": total_params,
            "optimizer": optimizer_name,
            "learning_rate": lr_value,
        }

        logger.info(
            "Training started for run '%s' (%s, %d params)",
            self.name,
            model_name,
            total_params,
        )

    def on_epoch_end(self, epoch: int, logs: Optional[dict] = None) -> None:
        step = dict(logs or {})
        step["epoch"] = epoch
        self._steps.append(step)

    def on_train_end(self, logs: Optional[dict] = None) -> None:
        end_time = datetime.datetime.now()
        duration = (end_time - self._start_time).total_seconds()

        run_data = {
            "name": self.name,
            "tags": self.tags,
            "environment": {
                "python": platform.python_version(),
                "tensorflow": tf.__version__,
            },
            "model": self._model_info,
            "start": self._start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration_seconds": duration,
            "steps": self._steps,
        }

        from blackboxml.store import save_run
        save_run(run_data, self.log_dir)
