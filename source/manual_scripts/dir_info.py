from source.script_interface import ScriptInterface
from pathlib import Path
from source.common import file_info
import pprint


class Script(ScriptInterface):
    def __init__(self) -> None:
        super().__init__()

    def run(self, folder: Path) -> None:
        for entry in folder.iterdir():
            if entry.is_dir():
                continue
            if entry.suffix not in ['.mkv', '.mp4']:
                continue

            self.print_file_info(entry)

    def print_file_info(self, file: Path) -> None:
        data = file_info(file)

        # pprint.pprint(data)

        print(f'FileName: {data['file_name']}')
        print('Tracks:')
        for track in data['tracks']:
            print(f'ID: {track['id']}, type: {track['type']}, language: {track['properties']['language']}')
