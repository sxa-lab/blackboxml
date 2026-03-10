import logging

logger = logging.getLogger("blackboxml")


class MetricStore:
    """Accumulates batch-level metrics into epoch-level weighted averages."""

    def __init__(self) -> None:
        self._weighted_sums: dict[str, float] = {}
        self._counts: dict[str, float] = {}

    def update(self, metrics: dict[str, float], n: int = 1) -> None:
        """
        Accumulate metric values weighted by batch size.

        Args:
            metrics: Mapping of metric names to their batch values.
            n: Batch size used as weight.
        """
        for key, value in metrics.items():
            self._weighted_sums[key] = self._weighted_sums.get(key, 0.0) + value * n
            self._counts[key] = self._counts.get(key, 0.0) + n

    def compute(self) -> dict[str, float]:
        """
        Return the weighted average for each accumulated metric.

        Returns:
            Dictionary mapping metric names to their weighted averages.

        Raises:
            ValueError: If no updates have been recorded.
        """
        if not self._weighted_sums:
            raise ValueError("No metrics have been recorded. Call update() first.")

        return {
            key: self._weighted_sums[key] / self._counts[key]
            for key in self._weighted_sums
        }

    def reset(self) -> None:
        """Zero all accumulators for the next epoch."""
        self._weighted_sums.clear()
        self._counts.clear()
