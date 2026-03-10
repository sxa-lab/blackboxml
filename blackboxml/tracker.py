from __future__ import annotations

import functools
import inspect
import logging
import platform
import subprocess
from datetime import datetime, timezone
from typing import Any, Callable

from blackboxml.store import save_run

logger = logging.getLogger("blackboxml")


def _git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def _git_dirty() -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return bool(result.stdout.strip())
    except FileNotFoundError:
        pass
    return None


def _framework_version(module_name: str) -> str | None:
    try:
        mod = __import__(module_name)
        return mod.__version__
    except (ImportError, AttributeError):
        return None


def _capture_environment() -> dict[str, Any]:
    return {
        "git_commit": _git_commit(),
        "git_dirty": _git_dirty(),
        "python": platform.python_version(),
        "torch": _framework_version("torch"),
        "tensorflow": _framework_version("tensorflow"),
        "hostname": platform.node(),
    }


class Run:
    """Context manager for logging training metrics."""

    def __init__(
        self,
        name: str,
        tags: list[str] | None = None,
        log_dir: str = "blackboxml_logs",
    ) -> None:
        self.name = name
        self.tags = tags or []
        self.log_dir = log_dir
        self._steps: list[dict[str, float]] = []
        self._start: datetime | None = None
        self._end: datetime | None = None
        self._environment: dict[str, Any] = {}

    def log(self, metrics: dict[str, float]) -> None:
        self._steps.append(metrics)

    def __enter__(self) -> Run:
        self._start = datetime.now(timezone.utc)
        self._environment = _capture_environment()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self._end = datetime.now(timezone.utc)
        duration = (self._end - self._start).total_seconds()

        run_data = {
            "name": self.name,
            "tags": self.tags,
            "environment": self._environment,
            "start": self._start.isoformat(),
            "end": self._end.isoformat(),
            "duration_seconds": duration,
            "steps": self._steps,
        }
        save_run(run_data, base_dir=self.log_dir)


def track(
    name: str,
    tags: list[str] | None = None,
    log_dir: str = "blackboxml_logs",
) -> Callable:
    """Decorator that wraps a generator function to automatically log yielded metrics.

    The decorated function must be a generator that yields metric dicts.
    Calling the decorated function creates a Run, consumes the generator,
    logs each yielded dict, and returns the list of all yielded metrics.
    """

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> list[dict[str, float]]:
            result = fn(*args, **kwargs)

            if not inspect.isgenerator(result):
                logger.warning(
                    "[BlackBoxML] @track expected a generator function, "
                    "but %s did not yield. No metrics were logged.",
                    fn.__qualname__,
                )
                return []

            collected: list[dict[str, float]] = []
            with Run(name=name, tags=tags, log_dir=log_dir) as run:
                for metrics in result:
                    run.log(metrics)
                    collected.append(metrics)
            return collected

        return wrapper

    return decorator
