from argparse import ArgumentParser
from pathlib import Path
from source.script_interface import ScriptInterface
from importlib import import_module


def load_scripts(scripts_folder: Path, scripts_module: str) -> dict[str, ScriptInterface]:
    out: dict[str, ScriptInterface] = {}
    for script_file in scripts_folder.iterdir():
        if script_file.is_dir():
            continue
        if '__' in script_file.name:
            continue

        if script_file.suffix != '.py':
            continue

        script: type[ScriptInterface]
        script = import_module(f'{scripts_module}.{script_file.stem}').Script
        out[script_file.stem] = script()

    return out


AUTO_SCRIPTS = load_scripts(Path(__file__).parent/'source'/'auto_scripts', 'source.auto_scripts')
MANUAL_SCRIPTS = load_scripts(Path(__file__).parent/'source'/'manual_scripts', 'source.manual_scripts')


def run_script(script: ScriptInterface, folder: Path, reraise: bool = False) -> int:
    try:
        script.run(folder)
    except (Exception, AssertionError):
        if reraise:
            raise
        return 1
    return 0


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument('mode', type=str, choices=['auto', 'manual'])
    parser.add_argument('folder', type=Path, help='Folder to process')
    parser.add_argument('--script', type=str, choices=MANUAL_SCRIPTS.keys(), help='Script to run (when manual mode is selected)', required=False)

    args = parser.parse_args()

    if args.mode == 'auto' and args.script is not None:
        print('Can not select script for automatic mode')
        return 1
    if args.mode == 'manual' and args.script is None:
        print('--script is required for manual mode')
        return 1

    if args.mode == 'manual':
        return run_script(MANUAL_SCRIPTS[args.script], args.folder, True)

    if args.mode == 'auto':
        for script in AUTO_SCRIPTS.values():
            if run_script(script, args.folder) == 0:
                return 0

    print('No suitable auto script found')
    return 1


if __name__ == '__main__':
    exit(main())
