from argparse import ArgumentParser
from pathlib import Path
from source.script_interface import ScriptInterface
from typing import Generator


def iterate_scripts() -> Generator[ScriptInterface, None, None]:
    scripts_folder = Path(__file__).parent/'source'/'scripts'
    for script_file in scripts_folder.iterdir():
        if script_file.is_dir():
            continue
        if '__' in script_file.name:
            continue

        script: type[ScriptInterface]
        script = __import__(f'source.scripts.{script_file.name}').Script
        yield script()


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument('folder', type=Path, required=True, help='Folder to process')

    args = parser.parse_args()

    for script in iterate_scripts():
        try:
            script.run(args.folder)
        except (Exception, AssertionError):
            continue
        return 0

    return 1


if __name__ == '__main__':
    exit(main())
