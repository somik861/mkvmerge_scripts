from subprocess import run
from dataclasses import dataclass
from typing import Any
from pathlib import Path
import json

@dataclass
class RunResult:
    stdout: str
    stderr: str
    return_code: int

def run_mkvmerge(*args) -> RunResult:
    rv = run(['mkvmerge', *args], capture_output=True, text=True)
    return RunResult(rv.stdout, rv.stderr, rv.returncode)

def file_info(file: Path) -> dict[str, Any]:
    rv = run_mkvmerge('-J', str(file))
    assert rv.return_code == 0
    return json.loads(rv.stdout)