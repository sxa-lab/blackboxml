import json
import os
import shutil
import tempfile

import pytest

from blackboxml.store import delete_all_runs, list_runs, load_run, save_run


@pytest.fixture
def tmp_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d, ignore_errors=True)


def _make_run_data(name="test_run"):
    return {
        "name": name,
        "tags": ["unit", "test"],
        "start": "2026-03-10T14:22:01",
        "end": "2026-03-10T14:35:47",
        "duration_seconds": 826,
        "steps": [{"loss": 0.5, "epoch": 0}],
    }


class TestSaveRun:
    def test_creates_run_json(self, tmp_dir):
        data = _make_run_data()
        path = save_run(data, base_dir=tmp_dir)
        assert os.path.isfile(path)
        assert path.endswith("run.json")

    def test_saved_data_matches(self, tmp_dir):
        data = _make_run_data()
        path = save_run(data, base_dir=tmp_dir)
        with open(path) as f:
            loaded = json.load(f)
        assert loaded["name"] == "test_run"
        assert loaded["steps"] == [{"loss": 0.5, "epoch": 0}]

    def test_sanitises_name(self, tmp_dir):
        data = _make_run_data(name="my run/with spaces!")
        path = save_run(data, base_dir=tmp_dir)
        assert "my_run_with_spaces_" in path


class TestLoadRun:
    def test_loads_valid_json(self, tmp_dir):
        data = _make_run_data()
        path = save_run(data, base_dir=tmp_dir)
        loaded = load_run(path)
        assert loaded["name"] == "test_run"

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_run("/nonexistent/run.json")

    def test_raises_on_corrupt_json(self, tmp_dir):
        bad_path = os.path.join(tmp_dir, "bad.json")
        with open(bad_path, "w") as f:
            f.write("not json{{{")
        with pytest.raises(json.JSONDecodeError):
            load_run(bad_path)


class TestListRuns:
    def test_returns_empty_for_missing_dir(self):
        assert list_runs("/nonexistent/dir") == []

    def test_lists_saved_runs(self, tmp_dir):
        save_run(_make_run_data("run_a"), base_dir=tmp_dir)
        save_run(_make_run_data("run_b"), base_dir=tmp_dir)
        runs = list_runs(tmp_dir)
        assert len(runs) == 2

    def test_sorted_newest_first(self, tmp_dir):
        save_run({**_make_run_data("older"), "start": "2026-01-01T00:00:00"}, base_dir=tmp_dir)
        save_run({**_make_run_data("newer"), "start": "2026-06-01T00:00:00"}, base_dir=tmp_dir)
        runs = list_runs(tmp_dir)
        assert runs[0]["name"] == "newer"


class TestDeleteAllRuns:
    def test_returns_zero_for_missing_dir(self):
        assert delete_all_runs("/nonexistent/dir") == 0

    def test_deletes_runs(self, tmp_dir):
        save_run(_make_run_data("a"), base_dir=tmp_dir)
        save_run(_make_run_data("b"), base_dir=tmp_dir)
        count = delete_all_runs(tmp_dir)
        assert count == 2
        assert not os.path.exists(tmp_dir)
