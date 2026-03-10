import json
import os
import shutil
import tempfile

import pytest

from blackboxml.tracker import Run, track


@pytest.fixture
def tmp_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d, ignore_errors=True)


class TestRun:
    def test_creates_run_json(self, tmp_dir):
        with Run(name="test_ctx", log_dir=tmp_dir) as run:
            run.log({"loss": 0.5})

        runs = os.listdir(tmp_dir)
        assert len(runs) == 1
        run_json = os.path.join(tmp_dir, runs[0], "run.json")
        assert os.path.isfile(run_json)

    def test_logs_multiple_steps(self, tmp_dir):
        with Run(name="multi_step", log_dir=tmp_dir) as run:
            run.log({"loss": 0.8})
            run.log({"loss": 0.6})
            run.log({"loss": 0.4})

        run_dir = os.listdir(tmp_dir)[0]
        with open(os.path.join(tmp_dir, run_dir, "run.json")) as f:
            data = json.load(f)
        assert len(data["steps"]) == 3

    def test_captures_environment(self, tmp_dir):
        with Run(name="env_test", log_dir=tmp_dir) as run:
            run.log({"loss": 0.5})

        run_dir = os.listdir(tmp_dir)[0]
        with open(os.path.join(tmp_dir, run_dir, "run.json")) as f:
            data = json.load(f)
        env = data["environment"]
        assert "python" in env
        assert "hostname" in env

    def test_records_timing(self, tmp_dir):
        with Run(name="timing_test", log_dir=tmp_dir) as run:
            run.log({"loss": 0.5})

        run_dir = os.listdir(tmp_dir)[0]
        with open(os.path.join(tmp_dir, run_dir, "run.json")) as f:
            data = json.load(f)
        assert "start" in data
        assert "end" in data
        assert data["duration_seconds"] >= 0

    def test_stores_tags(self, tmp_dir):
        with Run(name="tag_test", tags=["a", "b"], log_dir=tmp_dir) as run:
            pass

        run_dir = os.listdir(tmp_dir)[0]
        with open(os.path.join(tmp_dir, run_dir, "run.json")) as f:
            data = json.load(f)
        assert data["tags"] == ["a", "b"]


class TestTrackDecorator:
    def test_logs_yielded_metrics(self, tmp_dir):
        @track(name="deco_test", log_dir=tmp_dir)
        def train():
            yield {"loss": 0.8}
            yield {"loss": 0.5}

        result = train()
        assert len(result) == 2
        assert result[0]["loss"] == 0.8

    def test_creates_run_file(self, tmp_dir):
        @track(name="deco_file", log_dir=tmp_dir)
        def train():
            yield {"loss": 0.5}

        train()
        runs = os.listdir(tmp_dir)
        assert len(runs) == 1

    def test_warns_on_non_generator(self, tmp_dir):
        @track(name="not_gen", log_dir=tmp_dir)
        def train():
            return "not a generator"

        result = train()
        assert result == []
