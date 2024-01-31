from source.script_interface import ScriptInterface
from pathlib import Path


class Script(ScriptInterface):
    def __init__(self) -> None:
        super().__init__()

    def run(self, folder: Path) -> None:
        pass