import pytest

from blackboxml.metrics import MetricStore


class TestMetricStore:
    def test_single_update_and_compute(self):
        m = MetricStore()
        m.update({"loss": 0.5, "acc": 0.8})
        result = m.compute()
        assert result["loss"] == pytest.approx(0.5)
        assert result["acc"] == pytest.approx(0.8)

    def test_weighted_average(self):
        m = MetricStore()
        m.update({"loss": 1.0}, n=10)
        m.update({"loss": 0.0}, n=10)
        result = m.compute()
        assert result["loss"] == pytest.approx(0.5)

    def test_weighted_average_unequal_batches(self):
        m = MetricStore()
        m.update({"loss": 1.0}, n=30)
        m.update({"loss": 0.0}, n=10)
        result = m.compute()
        assert result["loss"] == pytest.approx(0.75)

    def test_reset_clears_state(self):
        m = MetricStore()
        m.update({"loss": 0.5})
        m.reset()
        with pytest.raises(ValueError):
            m.compute()

    def test_compute_raises_without_updates(self):
        m = MetricStore()
        with pytest.raises(ValueError):
            m.compute()

    def test_multiple_metrics(self):
        m = MetricStore()
        m.update({"loss": 0.4, "acc": 0.9}, n=5)
        m.update({"loss": 0.6, "acc": 0.7}, n=5)
        result = m.compute()
        assert result["loss"] == pytest.approx(0.5)
        assert result["acc"] == pytest.approx(0.8)
