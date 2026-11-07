"""provenance.json next to the output: code version, config and input hashes."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from . import __project__, __version__


def sha256(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(out_dir, config_path, inputs: list, extra: dict):
    rec = {
        "project": __project__, "script_version": __version__,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "config": Path(config_path).name, "config_sha256": sha256(config_path),
        "inputs": [{"file": str(p), "sha256": sha256(p)} for p in inputs if p],
        **extra,
    }
    (Path(out_dir) / "provenance.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
    return rec
