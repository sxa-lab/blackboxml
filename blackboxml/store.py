import os
import re
import json
import shutil
import logging

logger = logging.getLogger("blackboxml")


def _sanitise_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", name)


def save_run(run_data: dict, base_dir: str = "blackboxml_logs") -> str:
    """
    Persist a run to disk as JSON.

    Args:
        run_data: Must contain "name" (str) and "start" (ISO format timestamp).
        base_dir: Parent directory for all run directories.

    Returns:
        Path to the created run.json file.
    """
    name = _sanitise_name(run_data["name"])
    timestamp = run_data["start"].replace("-", "").replace(":", "").replace("T", "_")
    timestamp = timestamp.split(".")[0].replace(" ", "_")

    dir_name = f"{name}_{timestamp}"
    run_dir = os.path.join(base_dir, dir_name)
    os.makedirs(run_dir, exist_ok=True)

    run_path = os.path.join(run_dir, "run.json")
    with open(run_path, "w") as f:
        json.dump(run_data, f, indent=2)

    logger.info(f"[BlackBoxML] Run saved to {run_path}")
    return run_path


def load_run(run_path: str) -> dict:
    """
    Read and parse a run.json file.

    Args:
        run_path: Path to a run.json file.

    Returns:
        Parsed run data dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(run_path, "r") as f:
        return json.load(f)


def list_runs(base_dir: str = "blackboxml_logs") -> list[dict]:
    """
    Scan base_dir for run directories and load each run.json.

    Args:
        base_dir: Parent directory containing run subdirectories.

    Returns:
        List of run data dicts sorted by start time, newest first.
        Empty list if base_dir does not exist.
    """
    if not os.path.isdir(base_dir):
        return []

    runs = []
    for entry in os.listdir(base_dir):
        run_path = os.path.join(base_dir, entry, "run.json")
        if os.path.isfile(run_path):
            try:
                runs.append(load_run(run_path))
            except (json.JSONDecodeError, FileNotFoundError):
                logger.warning(f"[BlackBoxML] Skipping unreadable run: {run_path}")

    runs.sort(key=lambda r: r.get("start", ""), reverse=True)
    return runs


def delete_all_runs(base_dir: str = "blackboxml_logs") -> int:
    """
    Delete the entire base_dir directory tree.

    Args:
        base_dir: Parent directory containing run subdirectories.

    Returns:
        Number of run directories deleted. 0 if base_dir does not exist.
    """
    if not os.path.isdir(base_dir):
        return 0

    count = 0
    for entry in os.listdir(base_dir):
        entry_path = os.path.join(base_dir, entry)
        if os.path.isdir(entry_path) and os.path.isfile(os.path.join(entry_path, "run.json")):
            count += 1

    shutil.rmtree(base_dir)
    logger.info(f"[BlackBoxML] Deleted {count} run(s) from {base_dir}")
    return count
