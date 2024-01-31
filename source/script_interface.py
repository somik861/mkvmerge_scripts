from pathlib import Path
class ScriptInterface:
    # raise Exception (or derived) or AssertionError when folder not supported
    def run(self, folder: Path) -> None:
        raise NotImplementedError